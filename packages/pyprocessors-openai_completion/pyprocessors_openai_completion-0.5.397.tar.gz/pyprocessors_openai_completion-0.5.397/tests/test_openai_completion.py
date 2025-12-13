import json
import os
from copy import deepcopy
from pathlib import Path

import pytest
import requests
from dirty_equals import HasLen, HasAttributes, IsList, IsPartialDict
from pymultirole_plugins.v1.schema import Document, DocumentList, AltText

from pyprocessors_openai_completion.openai_completion import (
    OpenAICompletionProcessor,
    OpenAICompletionParameters,
    OpenAIModel,
    flatten_document, OpenAIFunction, AzureOpenAICompletionProcessor, ApolloOpenAICompletionProcessor,
    DeepInfraOpenAICompletionProcessor, AzureOpenAICompletionParameters, ApolloOpenAICompletionParameters,
    CHAT_GPT_MODEL_ENUM, DeepInfraOpenAICompletionParameters
)


def test_openai_completion_basic():
    model = OpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == OpenAICompletionParameters

    model = AzureOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == AzureOpenAICompletionParameters

    model = DeepInfraOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepInfraOpenAICompletionParameters

    model = ApolloOpenAICompletionProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == ApolloOpenAICompletionParameters


def test_flatten_doc():
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/complexdoc.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        flatten = flatten_document(doc)
        assert flatten == IsPartialDict(
            text=doc.text,
            title=doc.title,
            metadata_foo=doc.metadata["foo"],
            altTexts_0_name=doc.altTexts[0].name,
        )


JINJA_PROMPTS = {
    "preserve_entities": """Generates several variants of the following context while preserving the given named entities. Each named entity must be between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
    "substitute_entities": """Generates several variants of the following context while substituting the given named entities by semantically similar named entities with the same label, for each variant insert the new named entities between square brackets using the notation [label:entity].
    Context: {{ doc.text }}
    {%- set entities=[] -%}
    {%- for a in doc.annotations -%}
      {%- do entities.append('[' + a.label + ':' + a.text + ']') -%}
    {%- endfor %}
    Given named entities using the notation [label:entity]: {{ entities|join(', ') }}
    Output language: {{ doc.metadata['language'] }}
    Output format: bullet list""",
}


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("typed_prompt", [p for p in JINJA_PROMPTS.items()])
def test_jinja_doc(typed_prompt):
    type = typed_prompt[0]
    prompt = typed_prompt[1]
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
        completion_altText=type,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/jinjadocs.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        docs = [Document(**jdoc) for jdoc in jdocs]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(6)
        sum_file = testdir / f"data/jinjadocs_{type}.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


def chunks(seq, size=1000):  # noqa
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))


@pytest.mark.skip(reason="Not a test")
def test_semeval_docs():
    start_at = 32
    parameters = OpenAICompletionParameters(
        max_tokens=3000,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/semeval_fa_da.json",
    )
    with source.open("r") as fin:
        jdocs = json.load(fin)
        for i, chunk in enumerate(chunks(jdocs, 10)):
            if i >= start_at:
                docs = [Document(**jdoc) for jdoc in chunk]
                for type, prompt in JINJA_PROMPTS.items():
                    parameters.prompt = prompt
                    parameters.completion_altText = type
                    docs = processor.process(docs, parameters)
                    # assert docs == HasLen(6)
                    sum_file = testdir / f"data/semeval_fa_da_{type}_{i}.json"
                    dl = DocumentList(__root__=docs)
                    with sum_file.open("w") as fout:
                        print(
                            dl.json(exclude_none=True, exclude_unset=True, indent=2),
                            file=fout,
                        )


@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_prompt(model):
    parameters = OpenAICompletionParameters(
        model=model, max_tokens=120, completion_altText="completion"
    )
    processor = OpenAICompletionProcessor()
    docs_with_prompts = [
        (
            Document(
                identifier="1",
                text="séisme de magnitude 7,8 a frappé la Turquie",
                metadata={"language": "fr"},
            ),
            "Peux tu écrire un article de presse concernant: $text",
        ),
        (
            Document(
                identifier="2",
                text="j'habite dans une maison",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires à: $text",
        ),
        (
            Document(
                identifier="3",
                text="il est né le 21 janvier 2000",
                metadata={"language": "fr"},
            ),
            "Peux tu me donner des phrases similaires en changeant le format de date à: $text",
        ),
        (
            Document(
                identifier="4",
                text="""Un nuage de fumée juste après l’explosion, le 1er juin 2019.
                Une déflagration dans une importante usine d’explosifs du centre de la Russie a fait au moins 79 blessés samedi 1er juin.
                L’explosion a eu lieu dans l’usine Kristall à Dzerzhinsk, une ville située à environ 400 kilomètres à l’est de Moscou, dans la région de Nijni-Novgorod.
                « Il y a eu une explosion technique dans l’un des ateliers, suivie d’un incendie qui s’est propagé sur une centaine de mètres carrés », a expliqué un porte-parole des services d’urgence.
                Des images circulant sur les réseaux sociaux montraient un énorme nuage de fumée après l’explosion.
                Cinq bâtiments de l’usine et près de 180 bâtiments résidentiels ont été endommagés par l’explosion, selon les autorités municipales. Une enquête pour de potentielles violations des normes de sécurité a été ouverte.
                Fragments de shrapnel Les blessés ont été soignés après avoir été atteints par des fragments issus de l’explosion, a précisé une porte-parole des autorités sanitaires citée par Interfax.
                « Nous parlons de blessures par shrapnel d’une gravité moyenne et modérée », a-t-elle précisé.
                Selon des représentants de Kristall, cinq personnes travaillaient dans la zone où s’est produite l’explosion. Elles ont pu être évacuées en sécurité.
                Les pompiers locaux ont rapporté n’avoir aucune information sur des personnes qui se trouveraient encore dans l’usine.
                """,
                metadata={"language": "fr"},
            ),
            "Peux résumer dans un style journalistique le texte suivant: $text",
        ),
        (
            Document(
                identifier="5",
                text="Paris is the capital of France and Emmanuel Macron is the president of the French Republic.",
                metadata={"language": "en"},
            ),
            "Can you find the names of people, organizations and locations in the following text:\n\n $text",
        ),
    ]
    docs = []
    for doc, prompt in docs_with_prompts:
        parameters.prompt = prompt
        doc0 = processor.process([doc], parameters)[0]
        docs.append(doc0)
        assert doc0.altTexts == IsList(
            HasAttributes(name=parameters.completion_altText)
        )
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"en_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_openai():
    parameters = OpenAICompletionParameters(
        system_prompt="Tu es un journaliste",
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_default.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
@pytest.mark.parametrize("model", [m for m in CHAT_GPT_MODEL_ENUM])
def test_openai_text(model):
    parameters = OpenAICompletionParameters(
        model=model,
        system_prompt="Tu es un journaliste",
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / f"fr_{model.value}.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


@pytest.mark.skip(reason="Not a test")
def test_runpod():
    parameters = OpenAICompletionParameters(
        base_url="https://u33htlbn4e1hwd-8000.proxy.runpod.net/v1",
        system_prompt="Tu es un journaliste",
        max_tokens=120,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_runpod.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)


# noqa: E501
@pytest.mark.skip(reason="Not a test")
def test_q_and_a():
    prompt = """Répondre à la question en utilisant les segments suivants et en citant les références.
    Question: {{ doc.altTexts[0].text }}
    Segments: {{ doc.text }}"""

    parameters = OpenAICompletionParameters(
        max_tokens=2000,
        completion_altText=None,
        prompt=prompt,
    )
    processor = OpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/question_segments.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        docs = [Document(**jdoc)]
        docs = processor.process(docs, parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/question_segments_answer.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_azure_endpoint():
    parameters = AzureOpenAICompletionParameters(
        system_prompt="Tu es un journaliste",
        max_tokens=1000,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = AzureOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_azure_gpt_4.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_apollo_endpoint():
    parameters = ApolloOpenAICompletionParameters(
        system_prompt="Tu es un journaliste",
        max_tokens=1000,
        best_of=3,
        n=3,
        completion_altText="completion",
    )
    processor = ApolloOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_apollo_gpt_4.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_deepinfra_endpoint():
    parameters = DeepInfraOpenAICompletionParameters(
        model='mistralai/Mistral-Nemo-Instruct-2407',
        max_tokens=100,
        completion_altText="completion",
    )
    processor = DeepInfraOpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Peux tu écrire un article de presse concernant: séisme de magnitude 7,8 a frappé la Turquie",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="Peux tu me donner des phrases similaires à: j'habite dans une maison",
            metadata={"language": "fr"},
        ),
    ]
    docs = processor.process(docs, parameters)
    assert docs == HasLen(2)
    for doc in docs:
        assert doc.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
    testdir = Path(__file__).parent / "data"
    sum_file = testdir / "fr_nemo.json"
    dl = DocumentList(__root__=docs)
    with sum_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_direct_deepinfra():
    PROMPT = """[INST]Answer the question in french using the given segments of a long document and making references of those segments ["SEGMENT"] with the segment number. 
Be short and precise as possible. If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Question: Est-il prévu des congés rémunérés pour les femmes souffrant de douleurs menstruelles ?

SEGMENTS:
1. À l’heure où certaines entreprises ou même certaines collectivités prévoient des congés rémunérés pour les femmes souffrant de douleurs menstruelles importantes ou d’endométriose, une proposition de loi a été déposée au Sénat en ce sens le 18 avril 2023 par une sénatrice socialiste et plusieurs de ses collègues. Les femmes concernées pourraient faire l’objet d’un arrêt de travail ou encore télétravailler, sous certaines conditions. La proposition de loi prévoit aussi un congé payé pour les femmes (et leur conjoint) ayant subi une fausse couche.

2. La proposition de loi prévoit de créer un arrêt de travail indemnisé pour les femmes souffrant de dysménorrhée (règles douloureuses) ou d’endométriose (maladie gynécologique inflammatoire et chronique). Prescrit par un médecin ou une sage-femme, cet arrêt maladie autoriserait la salariée à interrompre son travail chaque fois qu’elle se trouverait dans l’incapacité physique de travailler, pour une durée ne pouvant excéder 2 jours par mois sur une période de 3 mois. Les IJSS, versées sans délai de carence, se calculeraient selon des règles dérogatoires favorables à la salariée.  Dans l’objectif d’éviter un arrêt de travail, la proposition de loi vise aussi à favoriser la possibilité de télétravail pour les femmes souffrant de règles douloureuses et invalidantes, via l'accord collectif ou la charte sur le télétravail lorsqu'il en existe un.    Enfin, le texte propose de créer sur justification, pour les femmes affectées par une interruption spontanée de grossesse, un congé rémunéré de 5 jours ouvrables. Le conjoint, concubin ou partenaire pacsé de la salariée aurait aussi droit à ce congé.    Reste à voir si cette 2e proposition de loi, déposée le 18 avril par une sénatrice socialiste et plusieurs de ses collègues, connaîtra un sort aussi favorable que la première.

3. Maternité, paternité, adoption, femmes enceintes dispensées de travail - L’employeur doit compléter une attestation de salaire lorsque le congé de maternité* débute (c. séc. soc. art. R. 331-5, renvoyant à c. séc. soc. art. R. 323-10).      Le même document est à compléter en cas de congé d’adoption*, de congé de paternité et d’accueil de l’enfant* ou, dans le cadre de la protection de la maternité, pour les femmes travaillant de nuit ou occupant des postes à risques dispensées de travail en raison d’une impossibilité de reclassement sur un poste de jour ou sans risques .      Il s’agit de la même attestation que celle prévue pour les arrêts maladie.

4. Grossesse pathologique liée au distilbène - Le distilbène (ou diéthylstilbestrol) prescrit il y a plusieurs années entraîne des grossesses pathologiques chez les femmes qui y ont été exposées in utero.      Les femmes chez lesquelles il est reconnu que la grossesse pathologique est liée à l’exposition in utero au distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32         ; décret 2006-773 du 30 juin 2006, JO 2 juillet).

5. Enfant né sans vie - L'indemnité journalière de maternité est allouée même si l'enfant n'est pas né vivant au terme de 22 semaines d'aménorrhée (c. séc. soc. art. R. 331-5). Pathologie liée au Distilbène - Bien que ce médicament ne soit plus prescrit, le Distilbène (ou diéthyltilbestrol) peut entraîner des grossesses pathologiques pour les femmes qui y ont été exposées in utero. Les femmes dont il est reconnu que la grossesse pathologique est liée à l’exposition in utero au Distilbène bénéficient d’un congé de maternité à compter du premier jour de leur arrêt de travail (loi 2004-1370 du 20 décembre 2004, art. 32, JO du 21). Ces femmes peuvent prétendre à l’IJSS de maternité dès le début de leur congé de maternité si elles remplissent les conditions d’ouverture du droit au congé légal de maternité (décret 2006-773 du 30 juin 2006, JO 2 juillet).

6. Possibilité de télétravailler pour les femmes souffrant de règles douloureuses Dans l’objectif d’éviter un arrêt de travail pour douleurs menstruelles, la proposition de loi vise à favoriser la possibilité de télétravail aux femmes souffrant de dysménorrhée (proposition de loi, art. 4).   À cet égard, l'accord collectif ou la charte sur le télétravail existant dans l’entreprise devrait préciser les modalités d’accès des salariées souffrant de règles douloureuses et invalidantes à une organisation en télétravail.    En toute logique, il ressort de l’exposé des motifs que cela ne viserait que les femmes dont l’activité professionnelle est compatible avec l’exercice du télétravail.      À noter : en dehors d’un accord ou d’une charte sur le télétravail, il est toujours possible à l’employeur et au salarié de convenir d’un recours au télétravail formalisé par tout moyen (c. trav. art. L. 1222-9).Une proposition de loi en faveur des femmes souffrant de douleurs menstruelles, d’endométriose, ou ayant subi une fausse couche
    [/INST]"""
    api_key = os.getenv("DEEPINFRA_OPENAI_API_KEY")
    deploy_infer_url = "https://api.deepinfra.com/v1/inference/meta-llama/Llama-2-70b-chat-hf"
    response = requests.post(deploy_infer_url, json={
        "input": PROMPT,
        "max_new_tokens": 4096,
        "temperature": 0.2
    },
                             headers={'Content-Type': "application/json",
                                      'Authorization': f"Bearer {api_key}"})
    if response.ok:
        result = response.json()
        texts = "\n".join([r['generated_text'] for r in result['results']])
        assert len(texts) > 0


# noqa: E501

@pytest.mark.skip(reason="Not a test")
def test_function_call_ner():
    candidate_labels = {
        'resource': 'RESOURCE',
        'organization': 'ORGANIZATION',
        'group': 'GROUP',
        'person': 'PERSON',
        'event': 'EVENT',
        'function': 'FUNCTION',
        'time': 'TIME'
    }
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/ner_long_prompt.txt",
    )
    with source.open("r") as fin:
        long_prompt = fin.read()

    parameters = OpenAICompletionParameters(
        model='gpt-4o-mini',
        max_tokens=4096,
        temperature=0.2,
        prompt=long_prompt,
        function=OpenAIFunction.add_annotations,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [
        Document(
            identifier="1",
            text="Selon l'agence de presse semi-officielle ISNA, les utilisateurs de carburant auraient reçu un message indiquant « cyberattaque 64411 », un numéro d'urgence lié au bureau du guide suprême iranien, l'ayatollah Ali Khamenei.",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="2",
            text="""En   Birmanie,   un   chauffeur   de   l'OMS,   l'Organisation   mondiale   de   la   santé,   qui   transportait   des 
échantillons de tests au coronavirus, a été tué dans une attaque dans l'État rakhine, une région en 
proie à des violences entre groupes rebelles et militaires.""",
            metadata={"language": "fr"},
        ),
        Document(
            identifier="3",
            text="""Un fonctionnaire du ministère de la Santé et des Sports, présent 
dans le véhicule, a été blessé.""",
            metadata={"language": "fr"},
        ),
    ]

    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    for a in doc0.annotations:
        assert a.text == doc0.text[a.start:a.end]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))

    source = Path(
        testdir,
        "data/ner_json_prompt.txt",
    )
    with source.open("r") as fin:
        json_prompt = fin.read()

    parameters.prompt = json_prompt
    parameters.function = None
    parameters.completion_altText = "json"
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))

    source = Path(
        testdir,
        "data/ner_xml_prompt.txt",
    )
    with source.open("r") as fin:
        xml_prompt = fin.read()
    parameters.prompt = xml_prompt
    parameters.function = None
    parameters.completion_altText = "xml"
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(3)
    doc0 = results[0]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.mark.skip(reason="Not a test")
def test_function_call_ner_v1():
    candidate_labels = {
        "radioisotope": "RADIOISOTOPE",
        "location": "LOCATION",
        "fuzzy_period": "FUZZY_PERIOD",
        "non_inf_disease": "NON_INF_DISEASE",
        "doc_source": "DOC_SOURCE",
        "doc_date": "DOC_DATE",
        "org_ref_to_loc": "ORG_REF_TO_LOC",
        "loc_ref_to_org": "LOC_REF_TO_ORG",
        "rel_date": "REL_DATE",
        "organization": "ORGANIZATION",
        "abs_period": "ABS_PERIOD",
        "rel_period": "REL_PERIOD",
        "pathogen": "PATHOGEN",
        "toxic_c_agent": "TOXIC_C_AGENT",
        "path_ref_to_dis": "PATH_REF_TO_DIS",
        "inf_disease": "INF_DISEASE",
        "abs_date": "ABS_DATE",
        "explosive": "EXPLOSIVE",
        "doc_author": "DOC_AUTHOR",
        "bio_toxin": "BIO_TOXIN",
        "dis_ref_to_path": "DIS_REF_TO_PATH",
    }
    testdir = Path(__file__).parent

    source = Path(
        testdir,
        "data/ner_long_prompt_inline.txt",
    )
    with source.open("r") as fin:
        long_prompt_inline = fin.read()

    source = Path(testdir, "data/evalLLM1.json")

    with source.open("r") as fin:
        jdoc = json.load(fin)
    doc = Document(**jdoc)
    doc.altTexts = [AltText(name='Segments', text=long_prompt_inline)]

    docs = [doc]

    source = Path(
        testdir,
        "data/ner_long_prompt_v1.txt",
    )
    with source.open("r") as fin:
        long_prompt = fin.read()

    parameters = DeepInfraOpenAICompletionParameters(
        model='meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8',
        max_tokens=16000,
        temperature=0.2,
        prompt=long_prompt,
        function=OpenAIFunction.add_annotations,
        candidate_labels=candidate_labels
    )
    processor = DeepInfraOpenAICompletionProcessor()
    results = processor.process(deepcopy(docs), parameters)
    assert results == HasLen(1)
    doc0 = results[0]
    for a in doc0.annotations:
        assert a.text == doc0.text[a.start:a.end]
    result_file = source.with_suffix(".json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))


@pytest.fixture
def expected_en():
    return {
        "Sport": "The french team is going to win Euro 2021 football tournament",
        "Politics": "Who are you voting for in 2021?",
        "Science": "Coronavirus vaccine research are progressing",
    }


@pytest.mark.skip(reason="Not a test")
def test_function_call_cat(expected_en):
    candidate_labels = {
        'sport': 'Sport',
        'politics': 'Politics',
        'science': 'Science',
    }

    EXCL_CLAUSE = "\nThe task is exclusive, so only choose one label from what I provided and write it as a single line.\n"
    NO_EXCL_CLAUSE = "\nThe task is not exclusive, so if more than one label is possible, please just write one label per line.\n"

    excl_prompt = """You are an expert Text Classification system. Your task is to accept Text as input and provide a category for the text based on the predefined labels.
{%- set labels=[] -%}
{%- for l in parameters.candidate_labels.values() -%}
  {%- do labels.append('"' + l + '"') -%}
{%- endfor %}
Classify the text below to one of the following labels: {{ labels|join(', ') }}
The task is exclusive, so only choose one label from what I provided and write it as a single line.""" + EXCL_CLAUSE + """Text: {{doc.text}}
Result:
"""
    no_excl_prompt = """You are an expert Text Classification system. Your task is to accept Text as input and provide a category for the text based on the predefined labels.
    {%- set labels=[] -%}
    {%- for l in parameters.candidate_labels.values() -%}
      {%- do labels.append('"' + l + '"') -%}
    {%- endfor %}
    Classify the text below to one of the following labels: {{ labels|join(', ') }}
    The task is exclusive, so only choose one label from what I provided and write it as a single line.""" + NO_EXCL_CLAUSE + """Text: {{doc.text}}
    Result:
    """
    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo,
        completion_altText=None,
        prompt=excl_prompt,
        function=OpenAIFunction.add_categories,
        candidate_labels=candidate_labels
    )
    processor = OpenAICompletionProcessor()
    docs = [Document(text=t) for t in expected_en.values()]
    docs = processor.process(docs, parameters)
    for expected_label, doc in zip(expected_en.keys(), docs):
        assert doc.categories[0].label == expected_label

    parameters.prompt = no_excl_prompt
    docs = [Document(text=t) for t in expected_en.values()]
    docs = processor.process(docs, parameters)
    for expected_label, doc in zip(expected_en.keys(), docs):
        assert doc.categories[0].label == expected_label


@pytest.mark.skip(reason="Not a test")
def test_cairninfo():
    prompt = """Vous disposez d'un article de revue scientifique couvrant un sujet dans le domaine des sciences humaines et sociales ou des sciences dures.  L'article peut faire une ou plusieurs pages.
Vous devez écrire un long résumé en français d'une longueur de 600 mots minimum.
Le résumé doit expliquer les points clés de l'article. 
Utilisez un vocabulaire précis et varié.
Évitez les répétitions.
Le résumé doit être complet et transmettre toutes les idées développées dans l'article.
Texte : $text
"""

    parameters = DeepInfraOpenAICompletionParameters(
        model="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        max_tokens=6000,
        completion_altText="résumé",
        prompt=prompt,
    )
    processor = DeepInfraOpenAICompletionProcessor()
    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/cairninfo.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        docs = processor.process([doc], parameters)
        assert docs == HasLen(1)
        sum_file = testdir / "data/cairninfo_summary.json"
        dl = DocumentList(__root__=docs)
        with sum_file.open("w") as fout:
            print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
    # noqa: E501


@pytest.mark.skip(reason="Not a test")
def test_resume_mixtral():
    text = """Jérusalem, ville sainte contestée
La situation ecclésiale diverse et complexe
Matthias Vogt

Jérusalem, ville sainte de trois religions, lieu de la passion, de la mort et de la résurrection de Jésus Christ, berceau du christianisme, destination de pèlerinages de millions de chrétiens du monde entier, lieu de rêves pour beaucoup qui, pour des raisons sociales ou politiques ne peuvent s’y rendre dont les chrétientés de la majorité de pays arabes et de beaucoup de pays qui se disent musulmans. Jérusalem, centre de la communauté chrétienne naissante dont témoignent les Actes des Apôtres, « Église-mère » de toutes les Églises, comme aiment à le répéter les clercs de la ville sainte, noyau de l’œcuménisme mais aussi point chaud de conflits interconfessionnels et foyer d’une communauté chrétienne multiforme. C’est sur la situation des Églises de Jérusalem et des chrétiens de la ville que nous voulons mettre l’accent dans cet article.
Situation actuelle de Jérusalem
De nos jours, Jérusalem est une ville d’environ 966 000 habitants dont la majorité sont juifs (567 000 ou 59 %) et environ 366 000 musulmans (38 %). Selon les données de l’année 2021 publiées par le Bureau israélien des statistiques, il y a à Jérusalem, Est et Ouest confondus, 12 900 chrétiens (1,3 % de la population totale), dont 9800 chrétiens arabes (ou 2,6 % de la population arabe). En 1944, les chrétiens comptent 19 % de la population (29 400 chrétiens parmi 30 600 musulmans et 97 000 juifs) ou quasiment la moitié de la population non-juive de la ville. Il faut donc constater une chute dramatique de la quote-part chrétienne. Ce qui pèse lourd chez les chrétiens de Jérusalem, c’est que cette ville considérée comme un « espace chrétien » n’existe plus, en tant que telle, depuis 1948 malgré la multitude d’églises, de lieux saints et d’institutions chrétiennes.
Pour les Juifs, Jérusalem est considérée la ville la plus conservatrice du pays. Avec son grand nombre d’écoles religieuses (yeshiva, pl. yeshivot), surtout dans le quartier juif de la vieille ville, le nombre croissant de quartiers ultra-orthodoxes à Jérusalem-Ouest et la présence de groupes nationalistes juifs à l’intérieur des murailles médiévales, l’ambiance dans la ville est de plus en plus hostile aux populations chrétienne et musulmane. Les implantations des colons nationalistes et religieux dans les quartiers chrétiens et musulmans de la vieille ville et dans les quartiers résidentiels arabes de Jérusalem-Est (surtout Sheikh Jarrah, Abu Tor et Silwan) constituent une provocation envers les habitants palestiniens et sont les lieux de multiples conflits violents entre colons, Palestiniens et forces de l’ordre israéliennes.
Pour les musulmans, Jérusalem se trouve au centre des préoccupations palestiniennes mais aussi mondiales vu l’importance des sanctuaires islamiques sur le Haram al-Sharîf. Deux mouvements islamiques extrémistes sont présents dans la ville : le Hamas (Mouvement de résistance islamique), né de la Société des Frères musulmans, et le Hizb al-tahrîr (Parti de la libération), mouvement islamique international, né en Palestine, qui vise à imposer l’application stricte de la loi islamique (sharî’a) et à établir un état islamique de type califal. Les deux mouvements se montrent peu favorables aux non-musulmans auxquels ils assignent, dans leur projet de cité, une place régie par les lois islamiques, c’est-à-dire un statut inférieur à celui des musulmans. Les manifestations des adhérents à ces deux mouvements, surtout aux alentours de la mosquée al-Aqsa, créent une ambiance peu rassurante pour les chrétiens de Jérusalem et remettent en question, de plus en plus, l’unité entre chrétiens et musulmans à cause du mouvement national palestinien.
Les Palestiniens de Jérusalem, chrétiens et musulmans, participent peu à la vie politique de la ville : dans les élections municipales les suffrages arabes sont bas, la participation à la chose publique étant considérée comme contribution à la « normalisation » d’une situation irrégulière. Ce n’est donc pas seulement à cause de la majorité absolue des habitants juifs de Jérusalem que la municipalité est dominée par la composante juive. Pour la politique israélienne, aussi bien sur le plan national que municipal, il n’y a aucun doute que Jérusalem est la « capitale éternelle et indivisible » de l’État juif telle que déclarée, en 1980, par la Knesset, le parlement israélien.
Les projets d’aménagement et de développement pris en charge par la municipalité de Jérusalem, sont considérés par la population arabe comme des tentatives plus ou moins dissimulées d’appropriation de terrains qui se trouvent encore entre les mains de propriétaires palestiniens. Des parcelles appartenant aux Églises ainsi qu’à des congrégations religieuses sont aussi menacées. Le projet d’aménagement d’un parc national sur les terrains pentus du Mont des Oliviers qui appartiennent à des Églises suscite l’inquiétude des chefs d’Églises. De même, l’acquisition par les associations de colons juifs d’immeubles, dans le quartier chrétien de la vieille ville, a suscité la critique des représentants des Églises. Même si certaines de ces transactions immobilières sont légales, les prix offerts, souvent le double du prix du marché, laissent apparaître un manque de droiture morale. La non-ingérence des autorités israéliennes compétentes trahit l’absence de volonté de protéger l’équilibre traditionnel et fragile des communautés religieuses dans la ville sainte.
La situation ecclésiale et œcuménique
Les chrétiens de Jérusalem se répartissent sur 13 communautés reconnues ; du côté orthodoxe : grecque, arménienne, syriaque, copte et éthiopienne ; du côté catholique : latine (catholique romaine), grec-melkite, arménienne, syriaque, maronite et chaldéenne ; du côté des Églises issues de la Réforme : épiscopale (anglicane) et luthérienne, sans compter différentes communautés protestantes et pentecôtistes non reconnues. Ces Églises comptent un nombre inégal de croyants de langue arabe vivant à Jérusalem : les catholiques de rite latin sont environ 5400 (55 %), les grecs orthodoxes 2300 (23 %), les melkites 860 (9 %), les arméniens orthodoxes 500 (5 %), les syriens orthodoxes 400 (4 %) et les autres 330 (3 %).
L’Église grecque-orthodoxe est dirigée par le patriarche de Jérusalem, assisté dans l’exercice de ses fonctions par 14 évêques titulaires. Ils sont tous membres de la Confrérie du Saint-Sépulcre (Confrérie des hagiotaphites) dont la mission est de préserver les propriétés de l’Église orthodoxe dans les lieux saints et de préserver le caractère hellénique du patriarcat. La communauté arabe est représentée dans la Confrérie par un seul évêque d’origine palestinienne ou jordanienne. Le fait que le clergé supérieur soit presque exclusivement grec, alors que les prêtres et les fidèles sont arabes, provoque régulièrement des tensions et des reproches de la part du laïcat selon lesquels la hiérarchie ne défend pas avec suffisamment de vigueur les intérêts de la communauté face à l’État israélien. Les activités sociales et humanitaires sont principalement menées par des associations de laïcs. Depuis les années 1990, les croyants arabes sont préoccupés par l’immigration en provenance des pays de l’ex-Union soviétique qui a entraîné une nette augmentation de communautés orthodoxes de langue non arabe. Ces fidèles vivent entièrement dans le milieu juif israélien et n’ont aucun contact avec les communautés arabes. Par leur présence, le caractère jusqu’alors presque exclusivement arabe de la communauté grecque-orthodoxe de Jérusalem et de Terre Sainte s’est affaibli. Cela ne renforce pas les prétentions des laïcs arabes d’avoir leur mot à dire dans la gestion des biens et leur demande d’arabisation du patriarcat.
L’Église romaine catholique (latine) est représentée par le patriarche latin de Jérusalem. Créé en 1099 pendant les croisades, le patriarcat latin a été rétabli en 1847. L’Église latine compte un grand nombre d’ordres et de congrégations (102 en 2018), souvent d’origine française et italienne. Elle gère de nombreuses institutions éducatives et sociales. Le patriarche de l’Église grecque melkite catholique se fait représenter à Jérusalem par un évêque avec le titre de protosyncelle, ayant juridiction sur la ville sainte et les territoires palestiniens. Les syriens catholiques et les arméniens catholiques ont tous les deux un exarque siégeant à Jérusalem. Les maronites vivent surtout dans le Nord d’Israël et c’est donc à Haïfa que réside leur évêque.
Les arméniens orthodoxes sont représentés à Jérusalem par un patriarche et un nombre de croyants inférieur à 1500. Ils se composent de trois éléments : les « anciens » arméniens de Terre Sainte, les descendants des réfugiés arméniens survivants du Génocide lors de la Première Guerre mondiale, et les immigrés arméniens venus après la chute de l’Union soviétique. Les arméniens vivent surtout dans leur quartier de la vieille ville et à Jérusalem-Ouest. Ils entretiennent des contacts avec la population palestinienne ou juive selon leurs préférences et leur lieu d’habitation. La plupart des arméniens venus avant 1948 se sentent solidaires des aspirations palestiniennes. L’organisation du patriarcat arménien repose avant tout sur la Confrérie de Saint Jacques et sur un conseil composé de dignitaires religieux appartenant à l’intérieur et à l’extérieur de la Terre Sainte.
Les syriaques et les coptes orthodoxes ont chacun un métropolite à Jérusalem. Depuis le milieu du XIXe siècle, l’Église copte se dispute avec l’Église éthiopienne la propriété du monastère de Deir al-Sultan située près du Saint-Sépulcre. La communauté éthiopienne a longtemps été composée d’un petit nombre de familles qui se retiraient dans les lieux saints afin de mener une vie de prière. En raison des bonnes relations politiques entre Israël et l’Éthiopie, un nombre important de travailleurs immigrés viennent en Israël et, depuis quelques années, de plus en plus de réfugiés. Les Éthiopiens vivent autour des monastères éthiopiens de Jérusalem-Ouest et de la vieille ville où ils se mêlent aussi bien avec les Juifs qu’avec les Arabes. Ils constituent ainsi une particularité parmi les chrétiens orientaux de Terre Sainte.
L’origine des évêchés épiscopal et luthérien remonte à un évêché commun anglican-luthérien, créé en 1841 par un accord entre la Grande-Bretagne et la Prusse. Cette dernière décidant de quitter l’union des Églises en 1886, l’Église anglicane en garde seule l’évêché. Aujourd’hui, la compétence de l’archevêque épiscopal de Jérusalem couvre la Palestine, Israël, la Jordanie, le Liban et la Syrie. La communauté luthérienne allemande a suivi sa propre voie, indépendamment de l’évêché anglican de Jérusalem, ses activités étant soutenues par le Jerusalemverein (Association de Jérusalem), créé à Berlin en 1853. Jusqu’à la Première Guerre mondiale, l’empereur Guillaume II a soutenu l’association et s’est lui-même rendu en Terre Sainte en 1898. À cette occasion, il a inauguré l’église protestante allemande du Rédempteur dans la vieille ville de Jérusalem. À la suite de ce voyage, est créée la fondation de l’impératrice Auguste Victoria, sur le Mont des Oliviers. La communauté évangélique arabe est issue, pour une part importante, de sortants de « l’Orphelinat syrien » de la famille Schneller. En 1929, naît la communauté évangélique palestinienne de Jérusalem, restée pourtant étroitement liée à la communauté luthérienne allemande. En 1958, se constitue l’Église luthérienne sous le nom d’Église évangélique luthérienne de Jordanie (Evangelical-Lutheran Church of Jordan, ELCJ) qui sera dirigée dès 1979 par un évêque dont le siège sera à Jérusalem.
La situation œcuménique à Jérusalem est considérée comme l’une des pires au monde. Des conflits sur les privilèges des Églises quant aux lieux saints ralentissent le rapprochement œcuménique. Un facteur extérieur rapproche pourtant les Églises de Terre Sainte l’une de l’autre depuis les années 1980 : la menace de « l’israélisation » de la ville sainte qui a forcé les chefs d’Églises de se montrer unis. Depuis de longues années, ont-ils pris l’habitude de publier des déclarations communes.
L’Assemblée des ordinaires catholiques de Terre Sainte a promulgué, en 2021, des directives œcuméniques. Elles visent surtout la participation des fidèles à la vie sacramentelle et prennent en considération la situation interconfessionnelle de beaucoup de familles chrétiennes. Sur le plan spirituel, on célèbre, à la fin janvier de chaque année, la semaine de l’unité des chrétiens par des prières communes, offertes à tour de rôle dans les églises de toutes les communautés chrétiennes. La situation exceptionnelle de la pandémie COVID-19 en mars 2020, a même donné l’occasion de dire une prière interreligieuse pour le salut de tous. Y ont participé les représentants de plusieurs Églises, les grands rabbins ashkénaze et séfarade, ainsi que des représentants de l’islam et des Druzes.
Jérusalem – Destination des pèlerins du monde entier
Le patriarcat grec-orthodoxe s’occupe de l’accueil des pèlerins orthodoxes. Reste à souligner la position particulière de l’Église russe-orthodoxe qui gère à Jérusalem plusieurs églises, monastères et hospices pour pèlerins (le fameux Russian Compound près de la Jaffa Street à Jérusalem-Ouest et l’église russe au pied du Mont des Oliviers), établis depuis la fin du XIXe siècle par la Société impériale orthodoxe de Palestine (fondée en 1882, confirmée et réformée la dernière fois en 2003). La société défend en Terre Sainte les intérêts du patriarcat de Moscou et s’occupe des pèlerins russes.
Côté catholique, la majorité des lieux saints sont gardés par les Franciscains de la Custodie (établie par le pape Clément VI en 1342). Avec l’aide de frères de différents pays, la Custodie dirige une bonne partie de la pastorale de pèlerins catholiques qui pratiquent diverses langues. À souligner aussi l’engagement social très important de la Custodie envers les chrétiens de Jérusalem, surtout dans le secteur de l’habitation et des bourses d’études.
Les pèlerins des pays arabes se sont faits rares depuis l’occupation de Jérusalem-Est par Israël en 1967. Le pape copte-orthodoxe Chenouda III (1971-2012) a interdit à ses fidèles le pèlerinage à Jérusalem au moment où l’Égypte et Israël concluaient un traité de paix en 1979. Le pape Tawadros (2012-), après s’être lui-même rendu à Jérusalem en 2015 à l’occasion des obsèques du métropolite copte, a levé cette interdiction en janvier 2022. Suite à cette mesure, 5000 Égyptiens approximativement se sont rendus à Jérusalem pour les célébrations pascales de 2022. Les chrétiens palestiniens se félicitent de cette présence de coreligionnaires arabes et la considèrent comme un renforcement important de leur position dans la ville sainte. Les pèlerins jordaniens, de leur part, sont peu nombreux. Ils peuvent demander des visas de groupe pour visiter les lieux saints à Jérusalem, en Israël et dans les territoires palestiniens, mais très peu en font usage. Aux fidèles du Liban et de la Syrie, la visite des lieux saints reste interdite, l’état de guerre qui règne toujours entre leurs pays et l’État d’Israël interdit toute communication avec l’État juif et ceci malgré la visite pastorale du patriarche Béchara Raï auprès de la communauté maronite d’Israël en 2014.
Le service religieux, l’entretien des églises, la préservation des droits de propriété et l’assistance aux pèlerins constitue une part importante du caractère des Églises de Jérusalem. Les droits de propriété et les privilèges sont régis par le « statu quo » de 1757, modifié en 1852. Cette réglementation n’a pas été modifiée, notamment parce que les Églises veillent jalousement sur leurs droits et privilèges. Ainsi les Églises grecque-orthodoxe, catholique, arménienne, copte, syriaque et éthiopienne jouissent-elles de droits sur des parties spécifiques de l’église du Saint-Sépulcre. En revanche, la clé se trouve depuis des siècles entre les mains de deux familles musulmanes. Les grecs, les arméniens, les coptes et les syriaques se partagent la propriété de l’église de la Nativité à Bethléem. Les catholiques n’ont qu’un droit d’accès à la grotte de la Nativité située sous la basilique. Mais ils ont leur propre église, directement rattachée à l’église byzantine. Les conflits interconfessionnels ont nettement diminué depuis que les travaux de restauration et de conservation, exécutés en entente cordiale par les différentes Églises dans l’édicule du Saint-Sépulcre (2016-2017), la basilique de la Nativité (2013-2020) et sous les pavées de la rotonde du Saint-Sépulcre (2022-), ce qui a renforcé le sentiment de confiance et de solidarité.
La vie sociale et politique des chrétiens de Jérusalem
Statut légal
Les chrétiens arabes de Jérusalem, comme tous les Palestiniens de la partie orientale de la ville, peuvent avoir un passeport jordanien. De plus, 52 % des chrétiens palestiniens de la ville sont titulaires d’une carte d’identité israélienne leur permettant la résidence permanente à Jérusalem, statut spécial accordé aux Palestiniens de Jérusalem après l’occupation israélienne de la ville en 1967. Depuis 2005, 44 % des chrétiens ont obtenu, en plus de cela, la citoyenneté israélienne (en 2005, seulement 5 % l’avaient). Ils hésitent donc entre leurs espoirs d’une future autonomie palestinienne dans Jérusalem-Est et les avantages que leur offre l’État juif. La citoyenneté israélienne leur offre l’accès au régime d’assurance nationale, au système de soins de santé, aux allocations de chômage et d’invalidité et aux prestations de retraite. Le choix de la citoyenneté israélienne n’est donc pas nécessairement lié à un changement d’opinion politique.
Les options de mariage des chrétiens de Jérusalem sont limitées par la loi israélienne, dite de « regroupement familial », promulguée en 2003. Cette loi empêche les familles non-juives d’obtenir des droits de résidence et d’entrée à Jérusalem. Elle porte également préjudice aux enfants nés dans les territoires palestiniens de parents résidant à Jérusalem-Est. Environ 300 familles chrétiennes de Jérusalem ont souffert de cette loi, en particulier les couples mariés après mai 2002. Il faut savoir que 16 % des familles chrétiennes de Jérusalem ont un parent originaire de Cisjordanie, principalement de Bethléem et de Ramallah. La loi restreint, de plus, les possibilités des chrétiens de Jérusalem de conclure des mariages avec un partenaire de la Cisjordanie. Étant donné les relations étroites entre familles chrétiennes hiérosolymitaines et bethléemites, cela est ressenti comme très douloureux et constitue une raison importante pour l’émigration des chrétiens. De nombreuses organisations internationales, israéliennes et palestiniennes, de défense des droits de l’homme ont fait pression contre cette loi, y compris la Société de Saint Yves (organisation de défense des droits de la personne sous les auspices du Patriarcat latin de Jérusalem) [12][12]Akroush, Jerusalem Christian Youth, 2019, p. 16..
La famille chrétienne
Depuis 2012, on constate une baisse du nombre de mariages chrétiens. Entre 2012 et 2019, on compte en moyenne chaque année 25 à 30 nouveaux mariages. L’âge médian des mariés chrétiens est de 29,2 ans pour les hommes et de 25,6 ans pour les femmes (données de 2016). 37 % de familles chrétiennes ont trois enfants, 31 % en ont quatre et 17 % deux. En comparant le taux de fécondité, les chrétiens ont le taux de fécondité le plus bas. Par conséquent, la communauté chrétienne de Jérusalem est, en moyenne, nettement plus âgée que la communauté musulmane (38 % des musulmans ont moins de 15 ans par rapport à 21 % des chrétiens). Quant aux personnes âgées (65 ans et plus), elles représentent 4 % de la population musulmane contre 14 % de la population chrétienne. L’âge médian dans la communauté chrétienne est de 34 ans, contre 21 ans dans la communauté musulmane.
La plupart des familles chrétiennes se présentent comme appartenant à la classe moyenne (90 %). Ceux qui s’identifient comme pauvres s’élèvent à 7 %. Dans plus de la moitié des familles chrétiennes (55 %), les deux parents travaillent, tandis que 44 % des familles n’ont qu’un seul soutien de famille, le plus souvent, c’est le père.
Les chrétiens arabes de Jérusalem vivent surtout en trois zones : au centre (vieille ville, Ras al-Amoud, Beit Faji), au Nord (Kufur Aqab, Anata, Beit Hanina, Shufat) et au Sud (Beit Safafa, Sharafat, Tantur). De plus en plus de familles chrétiennes achètent des propriétés dans les quartiers juifs, comme à Pisgat Ze’ev, ou acceptent de loger dans de nouveaux quartiers périphériques comme Talpiot-Est et Gilo. 30 % des familles chrétiennes sont propriétaires de leur appartement, 48 % vivent dans des appartements loués, tandis que 22 % habitent dans des propriétés « protégées » d’Église. Ces chiffres sont inquiétants si l’on considère que le taux d’accès à la propriété en Israël est de 66,5 %. Les coûts de loyer peuvent atteindre jusqu’à 40 % du revenu mensuel d’une famille, ce qui en fait la plus grande charge financière. Si l’on tient compte de tous les facteurs, on peut affirmer que plus de 60 % des familles chrétiennes sont menacées et vivent sous le seuil de la pauvreté. Elles peuvent à peine finir le mois sans dettes ou sans aide sociale de la part des Églises et des organisations caritatives.
Ainsi, près de 500 familles chrétiennes de Jérusalem reçoivent une aide financière sous diverses formes au moins une fois par an. Un quart des jeunes chrétiens reçoivent une aide financière de leurs Églises soit dans le cadre d’un programme d’aide sociale, soit sous la forme d’une aide aux études fournie par les Églises ou les écoles. La Custodie de Terre Sainte est le principal fournisseur de bourses d’études, offrant environ 40 bourses chaque année. Le patriarcat grec-orthodoxe offre plusieurs bourses d’études par an par le biais de l’école Saint Dimitri, mais pas nécessairement à des chrétiens. La Société de Saint-Vincent de Paul offre une dizaine de bourses d’études pour la formation professionnelle ou l’accueil de chrétiens pauvres. Le Secrétariat de solidarité, institution de l’Église catholique, offre des aides pour les frais de scolarité à plus de 2000 élèves chrétiens à Jérusalem, en Palestine, en Israël et en Jordanie.
Les écoles chrétiennes
La grande majorité des étudiants chrétiens de Jérusalem (98 %) sont inscrits dans des écoles chrétiennes. Cependant, on observe une tendance croissante parmi les Palestiniens – y compris les chrétiens – à s’inscrire dans les écoles gouvernementales israéliennes afin d’être mieux préparés au marché du travail israélien.
Les Églises et les organisations qui leur sont liées gèrent douze écoles à Jérusalem qui accueillent 1660 élèves chrétiens et plus de 5500 élèves musulmans. Huit de ces douze écoles sont situées dans et autour de la vieille ville. Les écoles chrétiennes sont le seul endroit où musulmans et chrétiens passent du temps ensemble, où ils peuvent faire connaissance au-delà de rencontres courtes et banales de tous les jours. Les écoles chrétiennes ont donc la responsabilité de promouvoir la coexistence, l’acceptation de l’autre et la démocratie, et d’enseigner l’histoire de la Terre Sainte dans une perspective chrétienne (y compris la période byzantine), ce qui ne fait partie ni du curriculum des écoles publiques israéliennes ni palestiniennes.
Par rapport aux autres écoles privées, municipales et islamiques (awqâf), les écoles chrétiennes jouissent d’une excellente réputation en termes de qualité de l’enseignement et en vue des certifications proposées, tant sur le plan local qu’international. Toutes les écoles chrétiennes suivent le programme palestinien, au moins jusqu’à la sixième année, avant de décider de s’engager ou dans le Tawjihi palestinien ou dans d’autres programmes tels que le General certificate of education (GCE) britannique, l’Abitur allemand (Schmidt’s Girls College), ou le Bagrut israélien. Les manuels palestiniens utilisés sont pourtant très déficitaires quant à la présentation des religions autres que l’islam et des périodes historiques anté-islamiques de la Palestine. Un rapport inédit du Centre œcuménique de théologie de la libération – Sabeel déplore que le curriculum palestinien qualifie chrétiens et juifs d’infidèles, qu’il préconise un califat islamique et qu’il insiste sur le port du hijab ou robe islamique. Un autre problème du système scolaire à Jérusalem-Est, y compris pour les écoles chrétiennes : à la fin de leurs études scolaires, à peine un tiers de chrétiens peuvent communiquer en hébreu alors que cette langue est la seule langue officielle dans les bureaux gouvernementaux et municipaux qui contrôlent tous les aspects de la vie à Jérusalem et en Israël.
En plus de leur rôle éducatif essentiel, les écoles chrétiennes sont sans doute les meilleurs forums pour la coexistence et la paix civile entre musulmans et chrétiens. Les musulmans qui étudient dans les écoles chrétiennes sont considérés comme les véritables agents de changement aux côtés de leurs concitoyens chrétiens. Les écoles chrétiennes s’investissent ainsi dans le développement d’êtres humains moralement responsables, et forment les meilleurs leaders de la société, démocratiques, énergiques et d’esprit ouvert quelle que soit leur croyance. Grâce à leur plus grande ouverture sur le monde vu le caractère international des congrégations religieuses ou institutions qui les soutiennent, les écoles chrétiennes de Jérusalem jouissent d’une plus grande liberté d’enseignement et vont au-delà des seuls textes éducatifs pour proposer à leurs étudiants des modèles de citoyenneté et des pratiques sociales et politiques qui favorisent la coexistence et la solidarité intercommunautaires.
Les Églises et leurs services
Malgré le nombre modeste de fidèles, les Églises en tant qu’institutions sont très fortes, grâce à la solidarité de l’Église universelle. Cela concerne les secteurs d’éducation, santé, culture, protection sociale et développement. Sur le plan culturel, il faut mentionner les nombreux centres communautaires, les clubs et les scouts, tous les trois régulièrement organisés selon les appartenances confessionnelles. Le secteur de la santé aussi joue un rôle important dans l’engagement des Églises qui gèrent cinq hôpitaux dans la ville sainte dont le plus grand est l’hôpital Auguste Victoria, géré par la Fédération luthérienne mondiale. Ces institutions emploient un total de 1200 salariés et accueillent plus de 330 000 patients par année, toute appartenance religieuse confondue.
Quant au secteur de la protection sociale, il concerne l’accueil et la réhabilitation de personnes handicapées, l’aide sociale, l’accueil de personnes âgées et la défense des droits de l’homme. À mentionner en particulier la Greek Orthodox Benevolent Society, le Good Samaritan Eldery Center situé dans un immeuble de la vieille ville appartenant au patriarcat grec-orthodoxe mais à vocation œcuménique, le foyer de personnes âgées des Sœurs de Notre Dame des Douleurs à Jérusalem-Est, les activités sociales de la Société de Saint Vincent de Paul, de Caritas Jérusalem et finalement la Société de Saint Yves pour la défense des droits de la personne (patriarcat latin de Jérusalem). Finalement, il faut mentionner les organisations internationales de développement à vocation chrétienne qui ont des branches ou bureaux à Jérusalem. Je ne peux conclure ce chapitre sans faire mention du Christian Information Center, tenu par la Custodie de Terre Sainte des Franciscains. Le centre s’occupe de la production médiatique, la distribution d’informations et de nouvelles sur tout ce qui concerne la vie chrétienne à Jérusalem, en Palestine et en Israël.
La vie des chrétiens en Israël et Palestine
Israël
L’image des chrétiens de Jérusalem serait incomplète sans un regard sur les chrétiens dans les territoires palestiniens et en Israël. Environ 127 000 chrétiens palestiniens vivent dans l’État d’Israël (sans Jérusalem-Est). La majorité d’entre eux vivent en Galilée, à Haïfa et dans les villes de Jaffa, Ramla et al-Ludd. Ils appartiennent majoritairement aux Églises grecques-melkites catholiques, grecques-orthodoxes et latines. Dans le Nord, il y a également quelques maronites. Ils jouissent de la citoyenneté israélienne et donc, en principe, des mêmes droits politiques et sociaux que ceux des israéliens juifs. Toutefois, en raison de diverses dispositions administratives subtiles, les localités majoritairement arabes d’Israël n’ont pas le même accès aux ressources financières du gouvernement que les municipalités juives. Néanmoins, la plupart des Palestiniens chrétiens se sont accommodés de l’État juif, apprécient les acquis sociaux, profitent de la situation économique d’Israël et jouissent de la liberté de voyager avec un passeport israélien. Ils s’engagent dans les partis arabes israéliens, sans pourtant se sentir liés, dans les élections, aux partis arabes. Ils votent aussi, selon les circonstances politiques, pour des partis majoritairement juifs de gauche et de droite, voire dans certains cas pour des partis juifs résolument religieux. Le processus d’intégration des chrétiens de Galilée dans l’État juif a commencé dès les années 1960. Aujourd’hui, rares sont les chrétiens de Galilée qui souhaiteraient échanger leur citoyenneté israélienne contre l’intégration dans un État palestinien, malgré la méfiance croissante de la population juive à l’égard des chrétiens à cause de la présentation biaisée du christianisme dans les écoles qui mettent un accent particulier sur la persécution des juifs dans les pays « chrétiens » pendant le Moyen-Âge et dans l’époque moderne et qui ne distinguent pas entre les chrétientés d’Occident et d’Orient. De nombreux chrétiens israéliens arabes sont préoccupés aussi par la propagation des idées islamistes au sein d’une partie de la population musulmane d’Israël. Cela a entraîné un fort recul de l’engagement politique commun entre chrétiens et musulmans. Les conflits entre musulmans, chrétiens et druzes sont également de plus en plus fréquents.
Au côté des chrétiens arabes d’Israël – et presque sans contact avec eux – vivent environ 420 000 Israéliens chrétiens de langue hébraïque. Ils sont principalement originaires des pays de l’ex-Union soviétique ainsi que des pays d’Europe de l’Est. La plupart d’entre eux sont russes orthodoxes. Ils sont tous citoyens israéliens et pleinement intégrés dans la société juive. S’y ajoutent environ 160 000 migrants chrétiens, dont beaucoup de femmes. Ceux-ci se composent de travailleurs migrants légaux et illégaux, originaires principalement d’Asie (Philippines, Inde, Sri Lanka) ; de demandeurs d’asile (surtout en provenance d’Érythrée et d’Éthiopie) ; de personnes qui, à la recherche d’un emploi, sont entrées avec un visa touristique déjà expiré (principalement d’Europe de l’Est, notamment de Roumanie et d’Ukraine). Les juifs convertis au christianisme constituent un groupe minuscule. Les chrétiens non-arabes installés de manière permanente en Israël représentent aujourd’hui environ un quart de la population chrétienne. Si l’on ajoute les travailleurs migrants et les demandeurs d’asile qui ne vivent que temporairement en Israël, ce groupe est même numériquement plus important que celui des chrétiens arabophones. Le plus grand groupe de migrants vit à Tel Aviv. C’est là qu’a été ouverte en 2015 une nouvelle église catholique avec un centre social pour les communautés de migrants. À Jérusalem, les migrants catholiques sont accueillis au centre « Ratisbonne » dans l’Ouest de la ville. De nombreuses communautés protestantes et évangéliques sont également actives en Israël. Leurs églises et lieux de culte sont souvent installés dans des magasins, des appartements et des abris anti-bombardement.
Les chrétiens représentent aujourd’hui près de 2 % de la population de l’État d’Israël (Jérusalem comprise). Si l’on y ajoute les migrants, ce chiffre atteint presque 4 %. Les juifs constituent 75 % de la population et les musulmans 18 %.
Telle est la complexité du christianisme en Israël. La loyauté envers l’État d’Israël, très répandue parmi les arabes chrétiens d’Israël, est régulièrement mise à l’épreuve. Les Palestiniens, chrétiens et musulmans de Cisjordanie, voient confirmé en ces occasions leur rejet par et de l’État juif. À titre d’exemple, citons la loi sur la nationalité adoptée par le Parlement israélien en 2018. Cette loi réaffirme le caractère juif de l’État, mais va encore plus loin en attribuant le droit à l’autodétermination nationale au seul peuple juif. Selon la nouvelle loi, la langue officielle est uniquement l’hébreu. L’arabe, qui est langue officielle depuis 1948, n’a plus qu’un statut particulier non défini. Certes, les conséquences pratiques de la loi sont marginales, puisqu’elle ne fait que confirmer ce qui va de soi dans l’esprit de la plupart des Juifs d’Israël. Elle n’en a pas moins un caractère hautement symbolique. C’est pourquoi elle a été vivement critiquée par les chefs d’Églises.
En mai 2021, le conflit déclenché par les expulsions de maisons palestiniennes dans le quartier arabe de Sheikh Jarrah à Jérusalem-Est et l’intervention musclée des forces de sécurité israéliennes lors de cérémonies du mois de Ramadan à la mosquée al-Aqsa ont profondément divisé les Juifs et les Arabes d’Israël. Du côté juif, on a eu peur des attaques de roquettes du Hamas. Du côté arabe, on était solidaire des victimes civiles des contre-attaques israéliennes à Gaza et des familles palestiniennes de Jérusalem-Est chassées de leurs maisons. Dans les villes mixtes d’Israël, où cohabitent Israéliens juifs et arabes, cela a donné lieu à de violentes émeutes et à des attaques lynchiennes de la part d’extrémistes juifs et arabes. Les gens des deux côtés avaient peur. Les chrétiens arabes d’Israël se sont retrouvés une fois de plus pris entre deux feux : solidarité avec le peuple palestinien dont ils font partie et loyauté envers l’État d’Israël, au sein des frontières dans lesquelles ils vivent. Les résultats des élections en Israël qui donnent des suffrages de plus en plus extrêmes et les annonces du gouvernement mises en place en décembre 2022 ne laissent présager rien de bon pour l’avenir de la cohabitation entre israéliens juifs et arabes de même que pour l’intégration des chrétiens arabes en Israël.
Palestine
Regardons encore la situation des chrétiens en Palestine, c’est-à-dire dans les territoires de Cisjordanie, administrés par l’Autorité palestinienne de Mahmoud Abbas, et dans la bande de Gaza, dirigée par un gouvernement Hamas. Y vivent environ 43 500 chrétiens (en 2008, des chiffres plus récents ne sont pas disponibles), dont moins de 1000 à Gaza. La population chrétienne de Cisjordanie se concentre dans la région de Bethléem avec Beit Jala et Beit Sahour ainsi qu’à Ramallah et dans les villages environnants. En Cisjordanie, les chrétiens représentent 1,5 % de la population parmi 98,5 % de musulmans. Dans la bande de Gaza, les chrétiens sont une infime minorité de moins de 0,1 % parmi une population presque entièrement musulmane. Les chrétiens sont pleinement intégrés dans la vie palestinienne et considèrent, pour la très grande majorité, l’État d’Israël et ses forces de sécurité comme des occupants. Ils souffrent beaucoup du blocus imposé par le mur de séparation qui coupe des territoires israéliens, les territoires contrôlés par l’Autorité palestinienne. De plus, les nombreux check-points israéliens font de la Cisjordanie « un patchwork » et rendent extrêmement long et compliqué le transport d’un endroit à l’autre. Dans ces conditions, les visites familiales, notamment aux nombreux chrétiens palestiniens vivant à Jérusalem, ne sont guère possibles, tout comme un contrat d’emploi en Israël. La bande de Gaza est même totalement isolée. De nombreux chrétiens de Palestine attribuent à la persistance du conflit israélo-palestinien, l’islamisation toujours plus poussée de la société palestinienne et de l’influence croissante de groupes islamistes extrémistes qui leur font peur.
Conclusions
Les Églises de Jérusalem peuvent-elles jouer un rôle de médiatrice pour la paix ? Le conflit au Proche-Orient n’est certes pas uniquement un conflit religieux. Mais les deux parties justifient leurs revendications en référence aux textes sacrés. Le conflit ne se comprend ni ne peut être résolu sans l’interférence de la religion. Certes, les référents religieux, du côté israélien et du côté palestinien ne sont pas les seuls, mais l’importance des revendications basées sur les arguments séculiers va en diminuant. Au cours des trois dernières décennies, l’essor du mouvement nationaliste religieux des colons juifs et la montée en puissance du Hamas, ont pris une ampleur angoissante. Cela ne manque pas d’avoir des répercussions sur la cohésion des Palestiniens chrétiens et musulmans. En fait, sans une participation constructive des religions, c’est-à-dire des leaders religieux et des organisations basées sur la foi religieuse, les tensions ne sauraient diminuer.
Quel rôle les Églises peuvent-elles jouer ? Au niveau mondial, les positions des Églises vis-à-vis du conflit israélo-arabe, sont loin d’être les mêmes. Beaucoup de chrétiens évangéliques américains soutiennent les revendications sionistes. Les Églises des pays arabes défendent le droit des Palestiniens. Le Vatican insiste sur le droit international et la décision de partage de l’ONU qui remonte à 1947. Il défend la position selon laquelle seuls Palestiniens et Israéliens ensemble peuvent parvenir à une autre solution par la voie de la négociation. Et l’Église de Jérusalem ? Elle aussi représente divers courants chrétiens : des chrétiens palestiniens en Palestine, des chrétiens arabes en Israël et des chrétiens de langue hébraïque en Israël, qui ont, chaque groupe pour sa part, des perspectives très différentes.
L’Église locale se trouve de plus en plus dans une situation de tension partagée entre les attentes des chrétiens de Palestine et de Jérusalem-Est d’une part et celles des chrétiens d’Israël d’autre part. Alors qu’en Palestine on attend que l’Église défende avec force les intérêts des Palestiniens, qu’elle dénonce les injustices et les violations du droit international, les Arabes israéliens s’identifient de plus en plus à l’État d’Israël et à ses réalisations sociales et économiques. La montée du Hamas et d’autres groupes islamistes à Gaza montre que les Églises pourraient jouer le rôle de médiateur. Les Églises doivent apprendre à gérer cette tension et les attentes divergentes de leurs fidèles. Elles pourraient ainsi jouer un rôle important de précurseur. La condition préalable est toutefois que les fossés confessionnels, particulièrement profonds en Terre Sainte pour des raisons historiques, soient enfin surmontés et que les Églises chrétiennes parviennent à une vraie entente œcuménique.

"""
    prompt = """Résume le texte ci-dessous en français. Le résumé doit faire environ 10% de l'article d'origine.
Output language: french
Text: $text
"""

    parameters = DeepInfraOpenAICompletionParameters(
        # model = "cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        max_tokens=512,
        completion_altText=None,
        prompt=prompt,
    )
    processor = DeepInfraOpenAICompletionProcessor()

    docs = processor.process([Document(text=text)], parameters=parameters)
    assert "Jerusalem" in docs[0].text


@pytest.mark.skip(reason="Not a test")
def test_explain_label():
    prompt = """Vous êtes un expert en classification de texte. Votre tâche consiste à fournir une explication en une phrase pour chacun des types d'événements décrits dans le texte en entrée.
La sortie doit être une table au format markdown dont la première colonne contient le type d'événement et la seconde colonne l'explication associée. Si aucun événement n'a été détecté, la sortie doit juste être "Aucun événement"
{%- set labels=[] -%}
{%- for cat in doc.categories -%}
  {%- do labels.append('"' + cat.label + '"') -%}
{%- endfor %}
{% if labels|length > 0 %}
Types d'événements à décrire: {{ labels|join(', ') }}
{%- else %}
Types d'événements à décrire: aucun
{%- endif %}
Texte: {{doc.text}}
    """
    parameters = OpenAICompletionParameters(
        model=OpenAIModel.gpt_3_5_turbo,
        completion_altText="explicationGPT",
        max_tokens=1024,
        prompt=prompt
    )
    processor = OpenAICompletionProcessor()

    parameters2 = DeepInfraOpenAICompletionParameters(
        model="cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        completion_altText="explicationMixtral",
        max_tokens=1024,
        prompt=prompt,
    )
    processor2 = DeepInfraOpenAICompletionProcessor()

    testdir = Path(__file__).parent
    source = Path(
        testdir,
        "data/event_detection-document-test.json",
    )
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
        docs = processor.process([doc], parameters)
        doc1 = docs[0]
        assert doc1.altTexts == IsList(HasAttributes(name=parameters.completion_altText))
        doc = Document(**jdoc)
        docs = processor2.process([doc], parameters2)
        doc2 = docs[0]
        assert doc2.altTexts == IsList(HasAttributes(name=parameters.completion_altText))


@pytest.mark.skip(reason="Not a test")
def test_evalllm():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/evalllm_2025_new_gpt_4_1-documents.json")

    with source.open("r") as fin:
        jdocs = json.load(fin)
    event_prompt = """
À partir du texte annoté en entité fourni à la fin, extrais chaque évènement suivant strictement les règles ci-dessous.

Un document peut contenir zéro, un ou plusieurs évènements.

Chaque évènement que tu extrais a un élément central correspondant à une entité avec éventuellement différents identifiants de mention.

L’élément central peut être :
- un agent du spectre NR/C/E (nucléaire-radiologique, chimique, explosif), correspondant à toute entité de type "radioisotope" ou "toxic_c_agent" ou "explosive",
- une maladie, correspondant à toute entité de type "path_ref_to_dis" ou "non_inf_disease" ou "inf_disease" ou "dis_ref_to_path",
- un agent pathogène (une entité de type "pathogen") ou une toxine (une entité de type "bio_toxin"), si le choix se présente, inclus cela en élément lié.

Chaque évènement que tu extrais a obligatoirement un lieu (une entité de type "location" ou "loc_ref_to_org") correspondant à une présence ou à une origine avérée ou potentielle de l'élément central.
Chaque évènement que tu extrais a facultativement tout autre élément lié correspondant strictement à :
- un élément naturel à la base de l'élément central,
- un élément naturel ayant engendré physiologiquement, même indirectement, l'élément central (ex : un agent pathogène, une toxine, une bactérie),
- la date à laquelle a eu lieu le seul évènement précisément extrait, correspondant à une entité de type "fuzzy_period" ou "rel_date" ou "abs_period" ou "rel_period" ou "abs_date" ou "doc_date".

Pour les éléments liés dans un évènement, ne conserve que la date la plus précise, par exemple : « 18/03/2021 » plutôt que « 18 mars »,  ou la zone géographique la plus petite, par exemple « Paris » plutôt que « France ». De même garde le lieu en toutes lettres plutôt que l’acronyme (ex : « République démocratique du Congo » VS « RDC »). Dans les cas particuliers des adresses postales, tous les éléments constitutifs de l’adresse doivent être inclus (rue/boulevard, lieu-dit, arrondissement, ville, etc.).

Ne doivent pas être liés :
- les éléments indirectement liés à l’évènement ou relevant de son contexte,
- les commentaires sur l’événement,
- les entités qui n’apportent pas d’information sur le risque lié à l’évènement, particulièrement les commentaires sur l’événement, les entités liées aux conférences de presse, réunions, analyses, procédures judiciaires, enquêtes, etc.

Tout élément d'un évènement doit être une entité annotée dans le texte fourni.

Mets ensemble au maximum les éléments directement constitutifs d'un seul et même évènement et tous les identifiants de mention correspondant à la même entité.

Vérifie bien que la composition de chaque évènement correspond strictement aux règles, si ce n'est pas la cas ne présente pas l'évènement concerné.

Fournis chaque évènement dans un format de données strictement comme ci-dessous.
{"central":[chaque numéro d'identifiant de mention correspondant à l'élément central de l'évènement],"associated":[[liste de numéro d'identifiant de mention d'un même élément lié]...]"}

Insère chaque évènement dans ce format à l'intérieur d'une liste, "[{...}...]".

Fournis seulement le résultat final sans aucun préfixe indiquant qu'il s'agit de code comme "```json".

Ci-dessous des exemples en référence

#Exemple#

##Texte annoté en entités##

 fr.euronews.com À vendre : <radioisotope id="euDoZG0Ang">uranium 238</radioisotope">, 200 millions d'euros ~1 minute   En <location id="dtPEACcPAJ">Géorgie</location">, 6 hommes ont été arrêtés après avoir voulu vendre de l’<radioisotope id="-z0UfOXhYQ">uranium 238</radioisotope">. Ils pensaient pouvoir le mettre en vente au prix de 200 millions de dollars et risquent aujourd’hui 10 ans de prison. L’<radioisotope id="mlARPsyH7S">uranium 238</radioisotope"> sert notamment à fabriquer du <radioisotope id="XQLKclyX3Z">plutonium 239</radioisotope">, capable de libérer une énorme quantité d‘énergie lors de la fission nucléaire. <fuzzy_period id="w0sDWYKMPs">Ces dernières années</fuzzy_period">, les pays du <location id="jOMRSOaemk">Caucase</location"> multiplient les arrestations d’individus impliqués dans des trafics de matières radioactives.

##Résultat##

[{"central": ["-z0UfOXhYQ", "euDoZG0Ang", "mlARPsyH7S"], "associated": [["dtPEACcPAJ"]]}]

#Exemple#

##Texte annoté en entités##

 <non_inf_disease id="64QddL5vUV">Botulisme</non_inf_disease"> : cinq personnes en réanimation pour une suspicion de <non_inf_disease id="4zeX8QtOq_">botulisme</non_inf_disease"> en <location id="gHygI5qPEq">Indre-et-Loire</location">, des bocaux de pesto à l’ail des ours mis en cause  <doc_source id="bCd6w2kpgD">Le Monde</doc_source"> Publié le <doc_date id="6FmuH33Tyi">10 septembre 2024</doc_date"> à 10h25, modifié le <doc_date id="OZO_xiZN5V">10 septembre 2024</doc_date"> à 20h06  Près de 600 produits de la marque <organization id="jghK9DAW6c">Ô Ptits Oignons</organization">, qui ont été vendus lors de quatre événements en <abs_period id="6JGQNl3WPQ">2024</abs_period">, sont cherchés dans toute la <location id="_x9A6NJuop">France</location">. « Les personnes qui [les] ont achetés doivent les jeter, les détruire », a déclaré le préfet.  Cinq personnes sont en réanimation au <org_ref_to_loc id="gf9WhUUplF">centre hospitalier de Tours</org_ref_to_loc"> pour une suspicion de <non_inf_disease id="w0M2zos9gQ">botulisme</non_inf_disease">, a annoncé Patrice Latron, le préfet d’<loc_ref_to_org id="sjP8hCt0js">Indre-et-Loire</loc_ref_to_org">, lors d’un point presse, <rel_date id="ygvIRzXMCf">mardi 10 septembre</rel_date">. Une enquête judiciaire a été ouverte.  « Deux couples se sont présentés aux urgences <rel_date id="-pvgk6rVbH">samedi</rel_date"> » et une cinquième personne, <rel_date id="qvR41tgpiB">dimanche</rel_date">, après avoir participé à un même « repas d’anniversaire », a précisé le préfet lors d’un point presse. Les patients, tous majeurs, « sont actuellement en réanimation, conscients, intubés, ventilés » au <org_ref_to_loc id="Rn-3rrL5Qu">centre hospitalier de Tours</org_ref_to_loc">, a détaillé le préfet.  « Sur la base d’indices convergents », les autorités sanitaires suspectent des cas de <non_inf_disease id="ikSWdboxW6">botulisme</non_inf_disease"> liés à l’ingestion « d’un produit [de la marque] <organization id="4qv7elJzs3">Ô p’tits Oignons</organization">, qui est un pesto à l’ail des ours, produit en <location id="3hvEOYngOM">Touraine</location"> », selon le préfet. Ce produit artisanal est « fortement suspecté d’être à l’origine de cette contamination », qui peut être mortelle, a-t-il souligné.  La priorité est désormais de « valider scientifiquement l’hypothèse du <non_inf_disease id="DFmjT9YpOV">botulisme</non_inf_disease"> et puis de leur assurer le meilleur traitement possible » ainsi que de faire de « la prévention pour éviter que d’autres personnes ne consomment le produit » suspecté. « Ce sont six cents bocaux que nous cherchons » sur toute la <location id="z0qqk_b6F0">France</location">, et « les personnes qui [les] ont achetés doivent les jeter, les détruire », a-t-il estimé. Alerte donnée au niveau national  Ils ont été vendus lors de quatre événements : la « Fête des Plantes et du Printemps » au <location id="1UhIAdbn9w">château de la Bourdaisière</location"> à <location id="20ioKwi81l">Montlouis-sur-Loire</location"> <fuzzy_period id="h-NwPVh9OK">fin mars</fuzzy_period">, la Fête « Nature en fête » au <location id="ZeChslvz18">château de Cangé</location"> à <location id="N1F4RdKC0Z">Saint-Avertin</location"> <fuzzy_period id="d7ogIP7WsW">mi-avril</fuzzy_period">, la « Foire à l’ail et au basilic » à <location id="MsUhb4-IJa">Tours</location"> <fuzzy_period id="kwa8xuZDTT">fin juillet</fuzzy_period"> et au « Festival de la tomate et des saveurs » au <location id="_17qZdn2ha">château de la Bourdaisière</location"> à <location id="IDUA--ncOe">Montlouis-sur-Loire</location">, qui s’est tenue <rel_date id="xwXWtUQtDg">samedi</rel_date"> et <rel_date id="kc_75audgc">dimanche</rel_date">, a-t-il dit.  « Le délai d’incubation de cette toxine est entre 4 heures et 8 jours », a-t-il rappelé, voulant « rassurer les personnes qui ont consommé ce produit <fuzzy_period id="ikxSIErPFa">il y a plusieurs semaines</fuzzy_period"> ».  Si les points de vente sont localisés au sein d’une même région, l’alerte a été donnée « immédiatement au niveau national avec un relais au niveau des ministères de la santé et de l’agriculture », selon le directeur de la santé publique pour l’<organization id="gwB_vTetSm-gBlATI-BfK">Agence régionale de santé (<organization id="d75B-8sfkg-gBlATI-BfK">ARS) du Centre-Val de Loire</organization"></organization">, Jean-Christophe Comboroure, lors de la même conférence de presse.  Quelque 30 % des bocaux ont été vendus par carte bleue et une équipe d’enquêteurs « sont en train de rechercher tous les clients et de les contacter », a signalé la directrice départementale de la protection des populations (DDPP) d’<loc_ref_to_org id="Gw3zosKXtu">Indre-et-Loire</loc_ref_to_org">, Carine Bar.  D’après M. Latron, une « enquête alimentaire » a « immédiatement été diligentée » entre l’<organization id="nMmtnr-f5-">ARS du Centre-Val de Loire</organization">, et les services de la DDPP. Elle est doublée d’une enquête judiciaire, a-t-il confirmé. Cette « enquête pénale », confiée à la <organization id="dL0N1C_CIU">direction interdépartementale de la police nationale</organization"> et la DDPP, retient « pour le moment » l’infraction de « blessures involontaires par personne morale suivies d’une incapacité supérieure à trois mois », selon la procureure de la République de <loc_ref_to_org id="N0CvtZoyyg">Tours</loc_ref_to_org">, Catherine Sorita-Minard. Aucune garde à vue n’a été effectuée, précise-t-elle, ajoutant que « les analyses se poursuivent » en vue de confirmer ou d’infirmer les suspicions de <non_inf_disease id="B9S8GukO6c">botulisme</non_inf_disease">. Affection rare et grave  Sur sa page Facebook, le producteur mis en cause s’est dit « sincèrement désolé » de cette situation. « A la suite d’un cas de <non_inf_disease id="uQCApKe81v">botulisme</non_inf_disease">, le pesto à l’ail des ours que je produis est peut-être en cause (…). Actuellement, ce n’est pas confirmé mais une forte suspicion » existe, a-t-il écrit.  Le <non_inf_disease id="_A6K6GVwHo">botulisme</non_inf_disease"> est une affection neurologique rare et grave, mortelle dans 5 % à 10 % des cas, provoquée par une toxine très puissante produite par une bactérie qui se développe notamment dans les aliments mal conservés, faute de stérilisation suffisante.  Elle engendre des problèmes oculaires (vision double), un défaut de déglutition et, dans les formes avancées, une paralysie des muscles, notamment respiratoires, qui peut conduire au décès.  En <abs_period id="BBJ0RWCs6M">septembre 2023</abs_period">, seize clients, dont une femme qui en est morte, ont été identifiés comme « cas suspects de <non_inf_disease id="nQL3nc4Ks7">botulisme</non_inf_disease"> » après avoir mangé des sardines en conserve de fabrication artisanale dans un restaurant touristique du centre de <location id="Ed5zfV7Z0y">Bordeaux</location">. En <location id="KAAlXTAd5O">France</location">, le <non_inf_disease id="8qWyLaXIhJ">botulisme</non_inf_disease"> est rare : l’incidence moyenne s’est stabilisée <rel_period id="5tD_uzBqON">depuis 1980</rel_period"> autour de 20-30 foyers par an, impliquant, le plus souvent chacun, un à trois malades.  D’après des données de l’<organization id="o7ORXXAhuM">Agence nationale de santé publique</organization">, <organization id="CJnQ_lCMke">Santé publique France</organization"> (<organization id="24Vb2znbMA">SPF</organization">), datant de <abs_period id="A9lMRuAq0a">2017</abs_period">, le taux d’incidence national est faible, s’élevant à 0,08 par million d’habitants. La maladie peut s’avérer grave lorsqu’elle n’est pas traitée à temps, et dans 5 % à 10 % des cas elle est mortelle, selon l’<organization id="mcpPffdvzn">Organisation mondiale de la santé</organization"> (<organization id="8s6K7FvJWy">OMS</organization">). L’affection est provoquée par une toxine, qui agit sur le système nerveux, produite par la bactérie <pathogen id="6XbDWO7gHe">Clostridium botulinum</pathogen">, explique <organization id="BC81i3DhJ6">SPF</organization">.

##Résultat##

[{"central": ["64QddL5vUV", "nQL3nc4Ks7", "DFmjT9YpOV", "B9S8GukO6c", "_A6K6GVwHo", "4zeX8QtOq_", "w0M2zos9gQ", "uQCApKe81v", "ikSWdboxW6", "8qWyLaXIhJ"], "associated": [["gHygI5qPEq"], ["gf9WhUUplF", "Rn-3rrL5Qu"], ["-pvgk6rVbH", "xwXWtUQtDg"], ["qvR41tgpiB", "kc_75audgc"], ["6XbDWO7gHe"]]}, {"central": ["64QddL5vUV", "nQL3nc4Ks7", "DFmjT9YpOV", "B9S8GukO6c", "_A6K6GVwHo", "4zeX8QtOq_", "w0M2zos9gQ", "uQCApKe81v", "ikSWdboxW6", "8qWyLaXIhJ"], "associated": [["Ed5zfV7Z0y"], ["6XbDWO7gHe"], ["BBJ0RWCs6M"]]}]

#Exemple#

##Texte annoté en entités##

 Cachotteries et soupçons autour du nuage radioactif russe <doc_source id="gGM7-q4M3e">Le Temps</doc_source"> 4–5 minutes  Publié le <doc_date id="6E-iI3czao">21 novembre 2017</doc_date"> à 20:54. / Modifié le <doc_date id="nFpTmUfYUp">10 juin 2023</doc_date"> à 15:24. Après plusieurs semaines de déni, la <loc_ref_to_org id="Ex23nQ4V7v">Russie</loc_ref_to_org"> reconnaît à demimot être à l’origine de la pollution radioactive détectée dans toute l’<location id="fpu2yzy1_N">Europe</location">. Mais continue à dissimuler la source et la raison exacte de cette fuite de <radioisotope id="LMzEHr9aGH">ruthénium-106</radioisotope">, un isotope qui n’existe pas dans la nature. Le <organization id="mA1KEgGeoN">service fédéral de météorologie</organization"> (<organization id="kFHqm-Ka9n">Rosgidromet</organization">) l’a admis <rel_date id="67p-PF_6A3">lundi</rel_date"> à travers une carte de la pollution, où le pic (près de 1000 fois la norme autorisée) se trouve dans le sud de l’<location id="M-8s7QCTFJ">Oural</location">, au niveau de la <location id="XIdVFChClQ">ville d’Argaïach</location">. Or, cette petite ville se trouve à une trentaine de kilomètres du site de retraitement nucléaire <org_ref_to_loc id="vrpBXL8gj6">Mayak</org_ref_to_loc">, de sinistre mémoire. L’explosion en <abs_period id="lAQPOIUv6Y">1957</abs_period"> d’un entrepôt de <radioisotope id="lQ6jv7OLF0">plutonium</radioisotope"> militaire avait lourdement contaminé l’environnement, causé 266 décès et entraîné l’évacuation de 10 000 personnes. Resté secret jusqu’en <abs_period id="wryxRS7y24">1991</abs_period">, il est classé comme le troisième plus grave accident de l’histoire nucléaire après Tchernobyl et Fukushima. Deux sources possibles L’<organization id="m2yim0r-YG">Institut de radioprotection et de sécurité nucléaire</organization"> (<organization id="CO54P36GxU">IRSN</organization">) français avait donné l’alerte en <rel_period id="cqJ6HgaL_e">octobre</rel_period">, précisant que les relevés anormaux apparaissaient <fuzzy_period id="OV5HXoIypt">dès le 25 septembre</fuzzy_period">. D’autres instituts à travers l’<location id="qFD1JOhSr-">Europe</location"> ont confirmé la présence d’un nuage radioactif venant soit de <location id="HnGeJvdT9S">Russie</location"> (<location id="AISnyFcg8M">Oural</location">), soit du nord du <location id="PEs6rPAZeg">Kazakhstan</location">. Dès le départ, les scientifiques européens ont lié ce type de pollution à deux sources possibles: des fuites lors de retraitement de carburant nucléaire ou venant d’équipement médical. Le <radioisotope id="bA3RxEdclA">ruthénium-106</radioisotope"> est utilisé notamment en radiothérapie pour éliminer certaines tumeurs. <organization id="2bc7UAdT-1">Rosgidromet</organization"> vend la mèche alors que la <loc_ref_to_org id="4Z9wP8-kVi">Russie</loc_ref_to_org"> s’est déjà positionnée pour une guerre de l’information. Le <rel_date id="NES2jFmyHA">11 octobre</rel_date">, l’agence d’Etat <organization id="KQz0uX2v4E">Rosatom</organization">, un géant industriel et énergétique contrôlant toute l’industrie nucléaire russe, dont <organization id="M53S2teJtW">Mayak</organization">, déclarait que la fuite venait non pas de <location id="wIHjwMz2Wp">Russie</location"> mais d’un « pays d’<location id="z-LPE6EwBG">Europe orientale</location"> », sous-entendant probablement l’<location id="mz7b-km1S4">Ukraine</location">, qui possède de nombreuses centrales nucléaires, dont <loc_ref_to_org id="pPGs9OjXww">Tchernobyl</loc_ref_to_org">. Par la suite, <organization id="9Cuf47_uCH">Rosatom</organization"> a indiqué que les relevés à travers la <location id="E39jiIPfOn">Russie</location"> ne comportaient aucune trace de <radioisotope id="Lanu5P1Rod">ruthénium-106</radioisotope">, hormis à <location id="TqiR-70AI6">Saint-Pétersbourg</location">, sur sa frontière occidentale avec l’<location id="MpSwxj8q8p">Europe</location">. L’agence d’Etat <organization id="qZUnJzULLA">RIA Novosti</organization"> titrait: « <organization id="8R8kPvUjkB">Rosatom</organization"> rejette la version occidentale sur la fuite de <radioisotope id="jEeZdHNJRq">ruthénium-106</radioisotope"> en <location id="DovVgGBvwj">Russie</location"> », comme s’il s’agissait d’accusations calomnieuses rituelles. « Aucune menace pour la santé » Conformément à une tradition soviétique, <organization id="wax-vC4Vxd">Mayak</organization"> s’est empressé de nier <rel_date id="6Kibku07Vn">mardi</rel_date"> toute responsabilité dans un communiqué destiné à impressionner les béotiens. «<organization id="MbPNYTzMfS">Mayak</organization"> n’a pas manipulé de sources de <radioisotope id="7sUH62TubY">ruthénium-106</radioisotope"> en <abs_period id="RlB8W0kANx">2017</abs_period"> (…) l’extraction de <radioisotope id="vEDnU1rJ2n">ruthénium-106</radioisotope"> à <organization id="Kj8drCQhNV">Mayak</organization"> a cessé <fuzzy_period id="WHd5EQHv6U">depuis de nombreuses années</fuzzy_period">.» Mais, prenant les devants, la centrale de retraitement souligne aussi que « les chiffres publiés par <organization id="KfPSvoYPeP">Rosgidromet</organization"> suggèrent que les doses que la population a pu recevoir sont 20 000 fois au-dessous de la dose annuelle admise et ne présentent aucune menace pour la santé ». Les experts occidentaux s’accordent à dire que les doses ne présentent apparemment pas de danger, ni pour l’homme ni pour l’environnement. En pointe sur l’observation de <organization id="f3Qc6Bublf">Mayak</organization">, <organization id="Yo0A1A02id">Greenpeace</organization"> admet que le sujet n’est pas la dangerosité pour la population. Mais l’ONG a réclamé auprès du parquet l’ouverture d’une enquête sur de possibles fuites et dissimulations. Le quotidien <organization id="WipF4IO8XL">Kommersant</organization"> rapporte une information venant de « défenseurs des droits humains » de la <location id="wp9ohNL5VW">région de Tcheliabinsk</location"> (où se trouve <org_ref_to_loc id="kf44WFg6Fg">Mayak</org_ref_to_loc">), selon laquelle de nouveaux containers de stockage de combustible retraité ont fait l’objet de tests les <rel_date id="kwJbL1Il6J-w9D3NcEK0W">24 et <rel_date id="7hr1zuvKnh-w9D3NcEK0W">25 septembre</rel_date"></rel_date">. Possible discrédit Les dénégations répétées de <organization id="6qhPygCAUR">Rosatom</organization"> pourraient aussi jeter le discrédit sur l’industrie nucléaire russe, alors que le monopole d’Etat affiche le premier carnet de commandes du monde en termes de construction de centrales nucléaires (100 milliards de dollars pour 25 pays-clients). <organization id="yLpDfvaDX-">Rosatom</organization"> a en outre annoncé <rel_date id="dlqdKJSzjc">mardi</rel_date"> un quintuplement de son programme d’investissement, soit 19 milliards de dollars d’ici à <abs_period id="ZxjmpqexTD">2023</abs_period">. Loin devant les géants énergétiques russes <organization id="Gv1bXKhMux">Rosneft</organization"> et <organization id="rw4g55PdfJ">Gazprom</organization">. En <location id="gl0nWMNCp_">Suisse</location">, la branche trading de <organization id="X5EmPylKtc">Rosatom</organization"> (<organization id="fA7FzXaugN">Uranium One</organization">) a ouvert un bureau à <location id="dHlKjwzfUQ">Zoug</location"> le <rel_period id="lNJojm-r_z">mois dernier</rel_period"> pour le négoce d’<radioisotope id="yPl07HQdlZ">uranium</radioisotope"> et de lithium.

##Résultat##

[{"central": ["fpu2yzy1_N", "MpSwxj8q8p", "qFD1JOhSr-"], "associated": [["bA3RxEdclA", "jEeZdHNJRq", "7sUH62TubY", "LMzEHr9aGH", "vEDnU1rJ2n", "Lanu5P1Rod"], ["OV5HXoIypt"], ["DovVgGBvwj", "HnGeJvdT9S", "E39jiIPfOn", "wIHjwMz2Wp"], ["PEs6rPAZeg"], ["TqiR-70AI6"]]}, {"central": ["lAQPOIUv6Y"], "associated": [["lQ6jv7OLF0"], ["kf44WFg6Fg", "vrpBXL8gj6"]]}]

#Exemple#

##Texte annoté en entités##

 <location id="wqKBdr9qF8">Cannes</location">: Deux lycéens, soupçonnés d’avoir fait exploser des engins artisanaux, placés en garde à vue  Illustration d'une voiture de police. - C. Allain / <organization id="Ka3OapvvXA">20 Minutes</organization"> / <doc_source id="M4-gfxNuCF">20 Minutes</doc_source"> <location id="Cz6dS8ZryE">Cannes</location">: Deux lycéens, soupçonnés d’avoir fait exploser des engins artisanaux, placés en garde à vue Le lycée avait dû être partiellement évacué ce <rel_date id="gWkMo2tIW3">jeudi</rel_date">. Deux internes du <organization id="uiCpnvVelm">lycée Bristol de Cannes</organization"> ont été placés en garde à vue <rel_date id="S_qq8-GFvp">vendredi</rel_date">, soupçonnés d’avoir fait exploser la veille des bouteilles remplies d’<toxic_c_agent id="55znmbTX9R">acide sulfurique</toxic_c_agent">. Les deux lycéens, mineurs, ont été interpellés à 14h55 et placés en garde à vue au <org_ref_to_loc id="VOyOdrmyl4">commissariat de Cannes</org_ref_to_loc"> où ils ont nié avoir fabriqué ces engins explosifs, a rapporté la procureur de <loc_ref_to_org id="lpJvE1qqkd">Grasse</loc_ref_to_org">, Fabienne Atzori, confirmant une information de <organization id="TPvzozDxFC">Nice-Matin</organization">. L’enquête doit être transférée à <location id="ahm4JXqViV">Nice</location">, la ville où résident ces deux lycéens en dehors des périodes scolaires. Des policiers scientifiques dépêchés sur place <rel_date id="Fjdveurbqc">Jeudi</rel_date">, l’explosion de deux bouteilles de Coca-Cola dans un couloir de l’établissement, remplies sans doute d’un mélange à base d’<toxic_c_agent id="KVaT_7wxWM">acide sulfurique</toxic_c_agent"> selon un tutoriel trouvé sur Internet, avait fait sursauter les élèves, sans faire de blessés. En application des procédures d’alerte, l’établissement avait connu un début d’évacuation. Le <organization id="VsiS_CzGZS">commissariat de Cannes</organization"> avait dépêché des policiers scientifiques sur place pour faire tous les prélèvements. Les cours avaient repris rapidement après l’intervention policière. <rel_date id="2A6a6dFTMB">Vendredi</rel_date">, une poubelle de l’établissement a par ailleurs été incendiée.

##Résultat##

[{"central": ["wqKBdr9qF8", "Cz6dS8ZryE"], "associated": [["gWkMo2tIW3", "Fjdveurbqc"], ["KVaT_7wxWM", "55znmbTX9R"]]}]

#Exemple#

##Texte annoté en entités##

 <pathogen id="OiA39vEVT1">Coronavirus</pathogen"> - Trump suspend tous les voyages de l'<location id="dVhoM2ZXox">Europe</location"> vers les <location id="0w13vQnfYb">Etats-Unis</location"> pour 30 jours <doc_date id="mjJ-DQGqRX">12/03/2020</doc_date"> &&& <doc_source id="rM8Wg0p1JN">AFP</doc_source">      Le président américain Donald Trump a annoncé <rel_date id="kBJABxL9nF">mercredi</rel_date"> la suspension pour 30 jours de tous les voyages depuis l'<location id="2W9K5gmx1P">Europe</location"> vers les <location id="iY1W0jcKtn">Etats-Unis</location"> afin d'endiguer l'épidémie de <path_ref_to_dis id="PIDee1Lkmd">nouveau coronavirus</path_ref_to_dis"> qui a de nouveau affolé les marchés financiers. "J'ai décidé de prendre des actions fortes mais nécessaires pour protéger la santé et le bien-être de tous les Américains", a annoncé M. Trump lors d'une allocution solennelle depuis le <org_ref_to_loc id="korYme3lEl">Bureau ovale de la Maison Blanche</org_ref_to_loc"> "Pour empêcher de nouveaux cas de pénétrer dans notre pays, je vais suspendre tous les voyages en provenance d'<location id="kHNGeLZLTZ">Europe</location"> vers les <location id="pcNzdl-8T6">Etats-Unis</location"> pour les 30 prochains jours", a-t-il ajouté, déplorant que l'<organization id="luz1ydJGeS">Union européenne</organization"> n'ait pas pris "les mêmes précautions" que les <loc_ref_to_org id="oRvpj64uut">Etats-Unis</loc_ref_to_org"> face à la propagation du virus. Cette mesure, qui entrera en vigueur <rel_date id="f7JLQH7twZ">vendredi</rel_date"> à minuit (04H00 GMT <rel_date id="XK83EMmNU7">samedi</rel_date">), ne concernera pas le <location id="0SxH7Hz0Oh">Royaume-Uni</location">, a précisé le milliardaire républicain. Au cours de son allocution de dix minutes, le président de la première puissance mondiale a qualifié le <pathogen id="rcqOiLreSo">nouveau coronavirus</pathogen"> de "virus étranger". <fuzzy_period id="yEIfdLmkIF">Il y a quelques jours</fuzzy_period">, le chef de la diplomatie américaine Mike Pompeo avait provoqué une polémique, et l'ire de <loc_ref_to_org id="MQrzbllA0j">Pékin</loc_ref_to_org">, en parlant de "virus de <location id="CaueooeYFe">Wuhan</location">". Le 45e président des <loc_ref_to_org id="AV6gKVhqJ2">Etats-Unis</loc_ref_to_org"> a achevé son discours en martelant sa conviction que l'avenir des <loc_ref_to_org id="o4qubcQ5vX">Etats-Unis</loc_ref_to_org"> restait "plus radieux que personne ne peut l'imaginer". Le président américain est accusé par nombre d'élus démocrates de vouloir minimiser à tout prix l'ampleur de la crise sanitaire à venir et d'envoyer des messages confus, parfois en contradiction avec ceux des autorités sanitaires. "Cela va disparaître, restez calme", avait-il encore déclaré <rel_date id="WODtSEM-JA">mardi</rel_date">. "Tout se déroule bien. Beaucoup de bonnes choses vont avoir lieu". M. Trump a par ailleurs appelé le <organization id="MuKBBAWBud">Congrès américain</organization"> à adopter rapidement une réduction des taxes sur les salaires pour aider les ménages américains à surmonter l'impact économique de l'épidémie de <path_ref_to_dis id="9penNgbgkH">coronavirus</path_ref_to_dis">. Cette proposition faite par son administration en <fuzzy_period id="gUyvkUjbaf">début de semaine</fuzzy_period"> n'a pas eu un écho très favorable auprès des élus, y compris de son propre parti. Le président a aussi annoncé le report de la date butoir de paiement des impôts pour certains individus et entreprises, qui devrait permettre selon lui de réinjecter 200 milliards de dollars de liquidités supplémentaires dans l'économie. <organization id="RlQe8BFi1p">Wall Street</organization"> a connu une nouvelle séance noire <rel_date id="4BQL2emogz">mercredi</rel_date">: le Dow Jones Industrial Average s'est effondré de 5,87%, à 23.550,74 points, et le Nasdaq a perdu 4,70%, à 7.952,05 points. Quelques heures avant l'allocution présidentielle, le directeur des <organization id="5n3ioZkOn4">Centres de détection et de prévention des maladies</organization"> (<organization id="NlBmUrJqG9">CDC</organization">) Robert Redfield avait estimé que le principal risque de propagation de l'épidémie pour les <location id="b8F3MbiWL8">Etats-Unis</location"> venait d'<location id="KvWIdL_6e9">Europe</location">. "La vraie menace pour nous, c'est désormais l'<location id="_eCj5lU8uv">Europe</location">", avait-il affirmé. "C'est de là qu'arrivent les cas. Pour dire les choses clairement, l'<location id="lO3SmM9GTQ">Europe</location"> est la nouvelle <location id="l2guquAMwQ">Chine</location">". <fuzzy_period id="DpKo-316Q0">Début février</fuzzy_period">, <loc_ref_to_org id="yR2V6Nu32k">Washington</loc_ref_to_org"> avait provisoirement interdit l'entrée aux <location id="BRM3tLOA4D">Etats-Unis</location"> des non-Américains s'étant récemment rendus en <location id="nB6743gUnN">Chine</location">. Le président Trump a longtemps invoqué cette décision drastique pour assurer que la propagation de l'épidémie était sous contrôle sur le <location id="R87YZwIm97">territoire américain</location">. Le <organization id="p46AX3FLmu">département d'Etat</organization"> a aussi recommandé aux ressortissants américains d'éviter les voyages non indispensables en <location id="OLqJF6Laio">Italie</location">, un avertissement aux voyageurs susceptible d'être au moins partiellement étendu au reste de l'<location id="z-6Cwph-Mc">Europe</location">. Les <location id="dEXCuh_Xzz">Etats-Unis</location"> ont dépassé <rel_date id="BAQ0sGiA5I">mercredi</rel_date"> la barre des 1.200 cas d'<inf_disease id="0LmbhIgB3C">infection au nouveau coronavirus</inf_disease">, et 38 personnes en sont mortes, selon les statistiques de l'<organization id="8l7zfatW19">université américaine Johns Hopkins</organization">.

##Résultat##

[{"central": ["R87YZwIm97", "dEXCuh_Xzz", "0w13vQnfYb", "BRM3tLOA4D", "pcNzdl-8T6", "b8F3MbiWL8", "iY1W0jcKtn"], "associated": [["4BQL2emogz", "kBJABxL9nF", "BAQ0sGiA5I"], ["PIDee1Lkmd", "9penNgbgkH", "0LmbhIgB3C"], ["rcqOiLreSo", "OiA39vEVT1"]]}]

#Exemple#

##Texte annoté en entités##

 Deux personnes hospitalisées suite à une fuite chimique à l'<org_ref_to_loc id="i-0kuXQFCi">AIA de Bordeaux</org_ref_to_loc"> Publié le <doc_date id="NnMnPNYm43">25/04/2015</doc_date"> à 16h30 Mis à jour le <doc_date id="7aj_OaRZVS">11/06/2020</doc_date"> à 00h51 Deux personnes travaillant à l'<organization id="ULaZO4taRD">AIA</organization"> (<organization id="B1iTHGnCq_">Atelier Industriel d'Aéronautique</organization">) se trouvent dans un état grave, suite à une fuite de produits chimiques. Le site, situé entre <location id="06juemy3yL">Floirac</location"> et <location id="8zKKPMZ9c0">Bordeaux</location">, dépend du <organization id="22_-6zgSAV">Minsitère de la Défense</organization">. Les pompiers sont à pied d'oeuvre depuis ce matin, 9 heures, sur le site de l'<org_ref_to_loc id="aMtWiMjcM3">AIA</org_ref_to_loc"> (<org_ref_to_loc id="8Tidkkwi3f">Atelier Industriel Aéronautique</org_ref_to_loc">) entre <location id="xqrpgEnMAm">Floirac</location"> et <location id="5yQ0HY40nt">Bordeaux</location">, en <location id="_ILrAb9xKB">Gironde</location">. En cause: une fuite d'<toxic_c_agent id="ya3icFy6dj">acide cyanhydrique</toxic_c_agent"> au sein de l'atelier 67. Deux personnes, âgées de 49 et 57 ans, ont été évacuées dans un état jugé "grave", dans un premier temps, vers l'<org_ref_to_loc id="J2wdDNU8yQ">hôpital bordelais Pellegrin</org_ref_to_loc">. Finalement, plus de peur que de mal, il s'avère que les deux salariés se portent bien. Un produit hautement toxique et dangereux L'<org_ref_to_loc id="ngR-o865wN">AIA</org_ref_to_loc"> est un site du <organization id="7o32JQbUMF">ministère de la Défense</organization">, le produit ayant causé des dégâts est utilisé pour polir les pièces d'avions militaires. Très toxique, cet acide a nécessité l'intervention de plus d'une vingtaine de pompiers, dont certains étaient spécialisés, ayant pour mission de le confiner et de déterminer l'origine de cette fuite.

##Résultat##

[{"central": ["ya3icFy6dj"], "associated": [["J2wdDNU8yQ"], ["NnMnPNYm43"]]}]

#Exemple#

##Texte annoté en entités##

 Du <toxic_c_agent id="i3xpjGk_lx">gaz moutarde</toxic_c_agent"> a été utilisé lors de combats en <location id="EHv53EDpmm">Syrie</location">, affirme l'<organization id="aod6OlqCVb">OIAC</organization">  L'<organization id="ZK5UNeLSBP">Organisation pour l'interdiction des armes chimiques</organization"> (<organization id="jcyByJJto2">OIAC</organization">) a confirmé que du <toxic_c_agent id="3A9GE-10Bt">gaz moutarde</toxic_c_agent"> avait été utilisé lors de combats en <location id="gySQySE85Q">Syrie</location"> en <rel_period id="JGiyzxpm1c">août dernier</rel_period">. Conformément à son statut, l'organisation n'a pas désigné de responsable. Publié le : <doc_date id="B41WAuH8Nu">06/11/2015</doc_date"> - 09:40	Modifié le : <doc_date id="ctiZFEWHCz">06/11/2015</doc_date"> - 16:26  Pour afficher ce contenu, il est nécessaire d'autoriser les cookies de mesure d'audience et de publicité. Du <toxic_c_agent id="aHS5_YA9xW">gaz moutarde</toxic_c_agent"> a été utilisé <rel_period id="kZfiQAssHp">cet été</rel_period"> lors de combats en <location id="Pi9GFdYknB">Syrie</location">, a confirmé pour la première fois <rel_date id="Y6FV5qz_vu">vendredi 6 novembre</rel_date"> l'<organization id="-4mzTmLAZA">Organisation pour l'interdiction des armes chimiques</organization"> (<organization id="KxmYgghwyT">OIAC</organization">), qui, conformément à son statut, n'a désigné aucun responsable.  Les experts en armes chimiques ont conclu que ce <toxic_c_agent id="DG0JnmLGUw">gaz asphyxiant</toxic_c_agent"> avait été utilisé le <rel_date id="WCrQgigSfD">21 août</rel_date"> à <location id="uHoO-GtC8-">Marea</location">, une ville de la <location id="TggxVyN5k8">province d'Alep</location">, dans le nord du pays. Un rapport encore confidentiel a été envoyé aux États membres de l'<organization id="vHTH19Vy8c">OIAC</organization">, qui doivent se réunir <fuzzy_period id="0wxrKjgy2W">fin novembre</fuzzy_period">. "On ne peut pas écarter l’hypothèse selon laquelle des stocks résiduels du programme militaire chimique syrien puissent être présents sur le théâtre des opérations et que l’un des belligérants ait pu mettre la main sur des petites quantités du stock", a expliqué sur <organization id="P-Py-Ezi-F">France 24</organization"> Olivier Le Pick, spécialiste des armes chimiques. Et d’ajouter, "on ne peut pas non plus écarter l’hypothèse d’une fabrication endogène. Contrairement au <toxic_c_agent id="S74-Kx2fTc">gaz sarin</toxic_c_agent"> qui a été utilisé dans la banlieue de <location id="0YK5fCg-Jb">Damas</location"> <fuzzy_period id="U-ItVcMfRE">il y a une dizaine de mois</fuzzy_period">, le <toxic_c_agent id="wFJJJ9BpQz">gaz moutarde</toxic_c_agent"> est beaucoup plus facile à synthétiser et il est à la portée de chimistes relativement peu compétents à fabriquer". Ce n'est d'ailleurs pas la première fois que l'usage du <toxic_c_agent id="zfk5zHhsnK">gaz moutarde</toxic_c_agent"> en <location id="v2hoLyhhdC">Syrie</location"> est évoqué. Des militants syriens et des ONG médicales avaient déjà affirmé <fuzzy_period id="ZHEOa7UKDW">fin août</fuzzy_period"> qu'une attaque à l'arme chimique avait touché des dizaines de personnes à <location id="czE31KAqn9">Marea</location">, où des combats opposaient des rebelles à des jihadistes de l'organisation de l'<organization id="XbpD-Al9QB">État islamique</organization"> (<organization id="W45HTdHhvq">EI</organization">). Accusations contre l'<organization id="Zo78GTlhyh">EI</organization"> Des patients soignés dans un hôpital d'<location id="JJr-j6GTBh">Alep</location"> rattaché à <organization id="wK-MxCP5X6">Médecins sans Frontières</organization"> avaient également évoqué un obus de mortier dégageant "un gaz jaune" dans leur maison. Selon des militants présents sur place au moment des faits, plus de 50 obus avaient été tirés ce jour-là sur <location id="8ihC2MUaf1">Marea</location"> par l'<organization id="LmcDwkRb7t">EI</organization">. Les accusations de recours aux armes chimiques par l'<organization id="F-ygnFm1yT">EI</organization"> se sont multipliées ces derniers mois en <location id="DVaKRQFOxL">Irak</location"> comme en <location id="GKJqUMFRFd">Syrie</location">, où le groupe jihadiste occupe de vastes régions. <loc_ref_to_org id="TDU2thuxdf">Washington</loc_ref_to_org">, <loc_ref_to_org id="yihe4JeH4M">Londres</loc_ref_to_org"> et <loc_ref_to_org id="-H6i9mzwf1">Paris</loc_ref_to_org"> avaient également accusé en <rel_period id="SSz0S26Fyg">août</rel_period"> le <organization id="mRpgKsKSls">régime syrien</organization"> d'avoir utilisé du <toxic_c_agent id="7Xk0NkK40X">gaz de chlore</toxic_c_agent"> contre des rebelles. Le <organization id="yqDNzh5FwO">régime syrien</organization"> est censé avoir détruit tout son arsenal chimique, aux termes d'un accord américano-russe de <abs_period id="6a0wLWMWqK">septembre 2013</abs_period"> qui lui a permis d'éviter des bombardements occidentaux - après, déjà, des accusations d'utilisation de <toxic_c_agent id="FWnDW4fv7q">chlore</toxic_c_agent">. Mais l'<organization id="3vZSblLHmw">OIAC</organization"> a conclu, en <abs_period id="-jII1k4fAx">2014</abs_period">, que du <toxic_c_agent id="lgcNPQxIvD">gaz de chlore</toxic_c_agent"> avait été utilisé dans le conflit. Déclenché en <abs_period id="5s_8TPE7LJ">2011</abs_period"> après la répression sanglante de manifestations réclamant des réformes, le conflit en <location id="a40Ea6ADoH">Syrie</location"> est devenu complexe au fil des années, avec une multiplication des acteurs, locaux et étrangers, sur un territoire de plus en plus morcelé. Il a causé la mort de plus de 250 000 personnes et poussé à la fuite des millions de Syriens. Avec <doc_source id="oblHB8xitv">AFP</doc_source">

##Résultat##

[{"central": ["wFJJJ9BpQz", "zfk5zHhsnK", "aHS5_YA9xW", "i3xpjGk_lx", "3A9GE-10Bt"], "associated": [["czE31KAqn9", "uHoO-GtC8-", "8ihC2MUaf1"], ["WCrQgigSfD"]]}, {"central": ["S74-Kx2fTc"], "associated": [["0YK5fCg-Jb"], ["U-ItVcMfRE"]]}, {"central": ["7Xk0NkK40X", "lgcNPQxIvD"], "associated": [["EHv53EDpmm", "GKJqUMFRFd", "a40Ea6ADoH", "v2hoLyhhdC", "Pi9GFdYknB", "gySQySE85Q"], ["5s_8TPE7LJ"], ["-jII1k4fAx"]]}]

#Exemple#

##Texte annoté en entités##

 Empoisonnement au <radioisotope id="7fSa7Af4H9">polonium</radioisotope"> : <loc_ref_to_org id="FLdy3rO-BR">Londres</loc_ref_to_org"> désigne Poutine <doc_source id="IBBe_0T4Wp">La Dépêche du Midi</doc_source"> 4–5 minutes  Publié le <doc_date id="Ho9T19TjQE">22/01/2016</doc_date"> à 07:30 , mis à jour à 08:14 <doc_source id="JW1w5c8sTf">La Dépêche du Midi</doc_source"> Il était mort dans d'atroces souffrances à l'<org_ref_to_loc id="B9UgWMSo9W">University College Hospital de Londres</org_ref_to_loc"> en <abs_period id="7t1OdrpUks">2006</abs_period">. Et l'on s'était rendu compte qu'Alexandre Litvinenko avait été victime d'un meurtre au <radioisotope id="bvp3veaM8v">Polonium 210</radioisotope">, un élément radioactif aussi rare que mortel, qui lui avait été administré dans des conditions rocambolesques, digne des pires romans d'espionnage. Du reste, Litvinenko était lui-même un ex-agent du <organization id="4XiwuySKis">KGB</organization">, et <rel_date id="IX76ZtuezD">hier</rel_date">, un juge de <location id="yNQqj6cKRe">Londres</location"> a assuré que Vladimir Poutine, le chef de l'<organization id="wojLlamC0e">État russe</organization"> ne pouvait pas ne pas être au courant de cette exécution. Dans le rapport de l'enquête publique, le magistrat a dit avoir réuni « des preuves qui établissent clairement la responsabilité de l'<organization id="EN81Rgljql">État russe</organization"> dans la mort de M. Litvinenko ». Le juge a ajouté que « l’opération du <organization id="jcUPTkrs-f">FSB</organization"> (successeur du <organization id="dQbm21ip2k">KGB</organization">) a probablement été approuvée par Nikolaï Patrouchev, ex-chef du <organization id="Ak2eaiFWFl">FSB</organization"> et aussi par le président Poutine ». Fureur à <loc_ref_to_org id="mZox7L1_qx">Moscou</loc_ref_to_org">, qui a aussitôt dénoncé une enquête « politiquement orientée », la qualifiant de «blague». Mais le <organization id="wSciAVR2Yl">gouvernement britannique</organization"> a convoqué l'ambassadeur de <loc_ref_to_org id="Nkxp0a0MgO">Russie</loc_ref_to_org"> à <location id="9VQuT1VjaU">Londres</location">. Et la ministre de l'Intérieur Theresa May a annoncé le gel des avoirs des deux exécutants présumés, Andreï Lougovoï et Dmitri Kovtoun. Les conclusions du juge disant « que le meurtre de l'ex-agent du <organization id="RCeEXoUqFp">KGB</organization"> Alexander Litvinenko a été autorisé au plus haut niveau de l'<organization id="VBme3Dhcn9">État russe</organization"> sont extrêmement dérangeantes », a réagi le porteparole du Premier ministre David Cameron. « Ce n'est pas une manière de se comporter, encore moins pour un pays qui est membre permanent du <organization id="qx8bp4xhq8">Conseil de Sécurité de l’ONU</organization"> », a-t-il insisté, sur un ton parfaitement britannique. La police a demandé l'extradition de Lougovoï et Kovtoun pour les juger, ce à quoi <loc_ref_to_org id="BDjmVBhrfM">Moscou</loc_ref_to_org"> s'est toujours refusé. La veuve de Litvinenko, Marina, a appelé <loc_ref_to_org id="-mcEkJ0SGV">Londres</loc_ref_to_org"> à aller plus loin en imposant « des sanctions économiques ciblées» à la <loc_ref_to_org id="j93FZ5QUpb">Russie</loc_ref_to_org"> et «des interdictions de voyage à MM. Patrouchev et Poutine notamment». Mais <loc_ref_to_org id="VO7Cbb2J0n">Londres</loc_ref_to_org"> doit aussi ménager un pays clef, engagé dans les négociations sur le conflit en <location id="z1M_IF6PK1">Syrie</location">, alors…  Le testament du mourant Juste avant de mourir, Litvinenko aurait rédigé une lettre posthume (à l‘authenticité contestée…) : « Vous pouvez réussir à me faire taire, mais ce silence a un prix. Vous vous êtes montrés aussi barbares et impitoyables que vos critiques les plus hostiles le prétendent. Vous avez montré que vous n'aviez pas de respect pour la vie, la liberté et les valeurs de la civilisation. Vous pouvez réussir à faire taire un homme mais les hurlements de protestation du monde entier retentiront à vos oreilles pendant le reste de votre vie, M. Poutine. ! »

##Résultat##

[{"central": ["bvp3veaM8v"], "associated": [["B9UgWMSo9W"], ["7t1OdrpUks"]]}]

#Exemple#

##Texte annoté en entités##

 Explosion à <location id="qj1b3zlgEs">Paris</location"> : le bilan s'aggrave et passe à au moins trois morts après le décès d'une touriste espagnole  Article rédigé par <doc_source id="nXdx06iSpp">franceinfo</doc_source"> <organization id="h32IXY0z5c">France Télévisions</organization"> Publié le <doc_date id="et5g0Vsnkg">12/01/2019</doc_date"> 09:31 Mis à jour le <doc_date id="D8uBFPPdkG">12/01/2019</doc_date"> 18:01  Selon le dernier bilan, deux pompiers sont morts, ainsi qu'une Espagnole. Par ailleurs, une cinquantaine de personnes ont été blessées.  Ce qu'il faut savoir Deux pompiers et une touriste espagnole sont morts dans la violente explosion qui a détruit une boulangerie à <location id="jQLIOeqS-G">Paris</location">, <rel_date id="D3ZMDd57XB">samedi 12 janvier</rel_date">. La très forte détonation a été entendue à 9 heures dans la <location id="UyWSdVvniR">rue de Trévise</location">, située dans le <location id="M3hYRqT4VO">9e arrondissement de la capitale</location">. Au moins neuf personnes sont en urgence absolue, dont un pompier, et 39 autres sont blessées. "Certains bâtiments sont vraiment détériorés et pourraient s'écrouler à tout moment, a prévenu en milieu d'après-midi le commandant Eric Moulin, des <organization id="EFnGFQLWy0">sapeurs-pompiers de Paris</organization">. Nous avons un doute sur la stabilité bâtimentaire de certains immeubles. C'est une zone sinistrée." Un incendie s'est déclenché dans une boulangerie et les pompiers sont intervenus à 8h37. Une violente explosion a alors retenti, détruisant l'immeuble et soufflant de nombreuses vitrines dans le quartier. Un bilan humain très lourd. Deux pompiers, âgés de 27 et 28 ans, sont morts. Une Espagnole qui faisait du tourisme, et dont l'identité n'a pas été divulguée, est décédée à l'hôpital. Une cause "manifestement accidentelle". Pour l'instant, la piste d'une fuite de gaz est privilégiée pour expliquer le sinistre, selon le procureur de la République de <loc_ref_to_org id="IRzqn5YbNn">Paris</loc_ref_to_org">. Une enquête a été confiée à la <organization id="P7q-qIziUl">direction régionale de la police judiciaire</organization">. Des vérifications sur les bâtiments alentour. Les secours tentaient encore de bloquer le gaz dans l'immeuble, des poches de gaz résiduelles ayant formé "des torchères à plusieurs niveaux du bâtiment", a expliqué le commandant Eric Moulin. Les architectes de sécurité procédaient également à des vérifications sur les bâtiments du quartier, pour "voir si tout allait bien". 1/2 2/2 2/2

##Résultat##

[]

#Exemple#

##Texte annoté en entités##

 Faits divers <location id="xk2gplnRTs">Rouffach</location"> : menace d'attentat à la bombe radioactive, un suspect en détention  Quatre bombes artisanales, dont trois prêtes à l'emploi, ont été découvertes le <rel_date id="3nFYrlfmdU">26 août</rel_date"> lors d'une perquisition dans une maison à <location id="dPWNHHmx-T">Rouffach</location">, a-t-on appris ce <rel_date id="r-5YEwAFsY">mercredi</rel_date"> matin de sources concordantes.  L'affaire remonte au <rel_date id="B0SX-9RGlb">26 août dernier</rel_date">. Ce matin-là, le <organization id="IUj2E3am_q">commissariat de Colmar</organization"> a reçu un appel du <organization id="GuUMc7gH3N">Centre de formation des apprentis de Colmar</organization">. L'un de ses élèves se serait vanté d'avoir confectionné plusieurs engins explosifs qu'il prévoyait d'utiliser contre des bâtiments publics. Selon un communiqué de la procureure de <loc_ref_to_org id="DluDJM1hLh">Colmar</loc_ref_to_org"> Catherine Sorita-Minard (lire ci-dessous), le jeune homme, né en <abs_period id="BmLPl2mOm4">1995</abs_period">, diffusait des vidéos sur ces explosifs.  Le suspect fréquentait le <org_ref_to_loc id="zRV0X5vaEq">Centre de formation des apprentis de Colmar</org_ref_to_loc">. Photo <organization id="6zf64dXcXw">L'Alsace</organization">  Les forces de l'ordre se sont rendues en milieu d'après-midi au domicile des parents du jeune homme à <location id="gh737NfA5M">Rouffach</location"> où ils découvrent les engins explosifs, a révélé <organization id="nUWqUH03Mk">Le Canard Enchaîné</organization"> dans son édition de <rel_date id="VM0ZgP3s27">mercredi</rel_date">. Une source proche de l'enquête a confirmé que le jeune homme affirmait, dans sa structure de formation, qu'il avait confectionné deux engins explosifs et qu'il voulait les faire sauter pour le <rel_date id="p_b-2wtgZ5">Nouvel An</rel_date">. Selon cette source, ces engins présentaient un réel risque d'explosion. Du minerai d'<radioisotope id="ECjm6Koe0W">uranium</radioisotope"> Les enquêteurs ont également trouvé du minerai d'<radioisotope id="SSs3Bebd46">uranium</radioisotope">. De quoi permettre de confectionner un engin explosif qui aurait pu propager de la radioactivité, sous une forme limitée. Ces opérations se sont déroulées dans le plus grand secret, les autorités craignant d'affoler la population. Écussons néonazis Aux enquêteurs, le jeune homme, âgé de 26 ans, a expliqué s'être fourni sur <organization id="hfKSrluV94">eBay</organization"> et avoir appris à confectionner ses engins explosifs à l'aide de tutoriels. Dans son logement, un studio également situé à <location id="B7Vg29ymdB">Rouffach</location">, selon le parquet, les policiers ont découvert des écussons nazis et une tenue complète du <organization id="ToF9BmzOJN">Ku Klux Klan</organization">. L'homme n'est pas fiché S ni connu comme actif dans le terrorisme. Le jeune homme s'est défendu en affirmant vouloir faire exploser ses bombes dans un champ ou un lieu neutre... Une information judiciaire a été ouverte pour fabrication d'engins explosifs. Il a été placé en détention provisoire. Suivi en médecine psychiatrique, il était inconnu des services de renseignement, mais connu des gendarmes comme un collectionneur compulsif. L'enquête a été confiée à la <organization id="KeAgwmHBDY">direction zonale de la police judiciaire Est</organization"> sur ordre du <organization id="2nqvI3Eu4m">parquet de Colmar</organization">.  Un suspect sans antécédent judiciaire Dans un communiqué diffusé ce <rel_date id="p-OBxPky7t">mercredi</rel_date"> après-midi, Catherine Sorita-Minard, procureure de la République de <loc_ref_to_org id="GMAO4o8ake">Colmar</loc_ref_to_org">, revient sur l'interpellation du jeune homme suspecté d'avoir fabriqué des engins explosifs à <location id="FrjEsl_gnq">Rouffach</location">.  « Le <abs_date id="_Cts3XY04A">26 août 2021</abs_date">, le <organization id="bUpnFvRPe8">parquet de Colmar</organization"> a été informé qu’un élève du <organization id="-BrJNXZb_t">Centre de Formation des Apprentis de Colmar</organization"> se vantait d’avoir fabriqué des engins explosifs, et diffusait des vidéos sur ce sujet. Il était rapidement identifié, localisé, interpellé et placé en garde à vue le jour même. Il s’agit d’un jeune homme né en <abs_period id="tObFBh3L5g">1995</abs_period"> à <location id="jFOigIVRyu">Colmar</location">, sans antécédent judiciaire, consommateur de stupéfiants ayant présenté par le passé des troubles psychiatriques ayant justifié des hospitalisations en psychiatrie. Des perquisitions ont été menées dans le temps de la garde à vue à <location id="5kvJcTjzZm">Rouffach</location"> où il est domicilié, permettant la découverte d’engins explosifs, d’ensembles de <explosive id="YFqnGeb6uk">poudres noires</explosive">, des initiateurs, des pièces métalliques, un morceau d’<radioisotope id="wtIgh5LpKi">uranium</radioisotope"> naturel. Les engins explosifs fabriqués ont été neutralisés par une équipe de démineurs. De nombreux matériels informatiques ont également été saisis, ainsi que de la documentation en lien avec le <organization id="A0Vnc2s8wB">Klu Klux Klan</organization">, certains documents étant ornés de croix gammée. Les faire exploser dans un champ Les premiers actes d’enquête ont été effectués par le <organization id="4iBAdPfhF4">commissariat de Colmar</organization">. J’ai ensuite saisi la <organization id="krat3iBQwy">direction zonale de la police judiciaire Est</organization"> aux fins de poursuite de l’enquête. L’intéressé a indiqué avoir fabriqué ces engins explosifs en vue de les faire exploser dans un champ ou dans des endroits neutres, sans danger pour les personnes ni pour les biens. Il a précisé avoir trouvé sur les réseaux sociaux les informations utiles pour fabriquer ces engins. Il apparaît en lien avec au moins une personne domiciliée en <location id="aLYETUxPCH">Belgique</location"> adhérant à des thèses d’ultra-droite. Il a été déféré au parquet le <rel_date id="vwIUiA-Gnj">28 août</rel_date">, et j’ai ouvert une information judiciaire des chefs suivants : · détention et transport de substances ou produit incendiaire ou explosif ou d’éléments servant à la confection d’engins explosifs · fabrication non autorisée d’engin explosif · fabrication d’éléments destinés à entrer dans la composition d’un produit explosif ».

##Résultat##

[{"central": ["SSs3Bebd46", "wtIgh5LpKi", "ECjm6Koe0W"], "associated": [["5kvJcTjzZm", "dPWNHHmx-T", "gh737NfA5M", "FrjEsl_gnq", "xk2gplnRTs", "B7Vg29ymdB"], ["_Cts3XY04A", "3nFYrlfmdU", "B0SX-9RGlb"]]}, {"central": ["5kvJcTjzZm", "dPWNHHmx-T", "gh737NfA5M", "FrjEsl_gnq", "xk2gplnRTs", "B7Vg29ymdB"], "associated": [["_Cts3XY04A", "3nFYrlfmdU", "B0SX-9RGlb"], ["YFqnGeb6uk"]]}]

#Exemple#

##Texte annoté en entités##

 L'explosion à <location id="pP4JS0TZak">Beyrouth</location"> a généré un cratère de 43 mètres de profondeur <doc_source id="_cjSLpuDM6">Le Temps</doc_source"> 4–5 minutes  1. Accueil 2. <location id="V5xtCYTzW7">Monde</location"> 3. <location id="-vc4eoo4Eb">Moyen-Orient</location"> Publié le <doc_date id="w24HH6Bm45">09 août 2020</doc_date"> à 10:12. / Modifié le <doc_date id="JVutCiceJD">09 août 2020</doc_date"> à 10:12. L'énorme explosion au <location id="-VmQodN2NL">port de Beyrouth</location"> a engendré un cratère de 43 mètres de profondeur, a indiqué <rel_date id="i0DTdyrryC">dimanche</rel_date"> une source sécuritaire libanaise, citant des évaluations effectuées par des experts français en pyrotechnie dépêchés sur le terrain. La déflagration survenue <rel_date id="cg4GoqZIU1">mardi</rel_date"> a fait plus de 150 morts et 6000 blessés, alors que des dizaines de personnes sont toujours portées disparues. Elle a été provoquée par l'explosion d'un entrepôt où étaient stockées selon le premier ministre libanais Hassan Diab 2.750 tonnes de <explosive id="LGoaNSV59T">nitrate d'ammonium</explosive"> depuis six ans « sans mesures de précaution ». La journée de <rel_date id="FJHyqYOk6J">samedi</rel_date">: Après une journée de colère à <location id="IRkBYBHyUp">Beyrouth</location">, le premier ministre annonce des élections anticipées Comme un séisme de 3,3 L'explosion « a provoqué un cratère de 43 mètres de profondeur », d'après la source de sécurité. L'<organization id="U75D2aeN_0">institut américain de géophysique</organization"> (<organization id="PxLGE24Zxk">USGS</organization">) basé en <location id="9gOapF6Vdh">Virginie</location"> avait indiqué que ses capteurs avaient enregistré l'explosion comme un séisme de 3,3 sur l'échelle de Richter. A titre de comparaison, l'explosion en <abs_period id="3N2Mf08VB3">1962</abs_period"> d'une bombe atomique de 104 kilotonnes sur le site d'essais nucléaires de « <location id="pVT79ZAstW">Sedan</location"> » au <location id="QeftYZ8V9X">Nevada</location"> (dans l'ouest des <location id="WH-LrCaBUN">Etats-Unis</location">), avait creusé un cratère de près de 100 mètres de profondeur.  © Haytham Al Achkar/<organization id="tXlGYxQ_65">Getty Images</organization"> Le spectaculaire attentat qui a tué l'ancien premier ministre Rafic Hariri en <abs_period id="907RQozSXj">2005</abs_period">, mené avec une camionnette bourrée d'explosifs, avait laissé un cratère d'au moins dix mètres de diamètre et de deux mètres de profondeur, selon le site Internet du <organization id="MuEcy8IZl-">Tribunal spécial international</organization"> (<organization id="aAH1ihHcpC">TSL</organization">). Lire aussi : Emilie Sueur: « Les Libanais demandent à la classe politique de se suicider » Colère dans la rue  © <organization id="fzjXYeoOld">AFP</organization"> <rel_date id="YWkVmlsiz2">Samedi</rel_date">, des milliers de manifestants en colère contre la classe dirigeante accusée de corruption, d'incompétence et de négligence après l'explosion, ont pris d'assaut brièvement des ministères et défilé dans le centre-ville de <location id="2jUuHpBEOB">Beyrouth</location"> pour crier vengeance. Ils ont brandi des potences de fortune symbolisant la rage à l'égard des dirigeants. Ce <rel_date id="1yUX81-Twf">dimanche</rel_date">, conférence des donateurs Des <loc_ref_to_org id="xIgQSI_Qsr">Etats-Unis</loc_ref_to_org"> à la <loc_ref_to_org id="EAMe7SVPDH">France</loc_ref_to_org"> en passant par la <loc_ref_to_org id="fCtTE9v3kd">Chine</loc_ref_to_org">, la <loc_ref_to_org id="se_JXbzwpb">Russie</loc_ref_to_org"> et l'<loc_ref_to_org id="nRofewtW_G">Egypte</loc_ref_to_org">, les donateurs internationaux se réunissent <rel_date id="A24DeZfrco">dimanche</rel_date"> pour une visioconférence de soutien au <loc_ref_to_org id="OXbtledc-Z">Liban</loc_ref_to_org">. La conférence en ligne, organisée à l'initiative de la <loc_ref_to_org id="8HPKOUQbsA">France</loc_ref_to_org"> et de l'<organization id="ce1E86K7_3">ONU</organization">, commence <rel_date id="bICyzTXAHM">dimanche</rel_date"> à 14h. Elle doit marquer le début d'une « démarche d'urgence et d'espoir pour l’avenir » du pays, a indiqué <rel_date id="FzEA4qTxqG">samedi</rel_date"> la <organization id="aO-rAtowXa">présidence française</organization">. Le président américain Donald Trump a annoncé qu'il participerait à cette réunion. « Tout le monde veut aider! » a-t-il tweeté, mentionnant avoir parlé avec le président français. <loc_ref_to_org id="IHwWi30Msk">Israël</loc_ref_to_org"> ne sera « pas dans le tour de table » de cette conférence, a-t-on précisé à l'<organization id="dmnNTVEyUh">Élysée</organization">, mais un contact est « pris par l’<organization id="nY20roZXag">ONU</organization"> ».  © ANWAR AMRO / european afp / <organization id="2O6dFGA7z1">AFP</organization"> Pour sa part, l'<loc_ref_to_org id="0Ic7x4O4V_">Iran</loc_ref_to_org"> n'a « pas manifesté sa volonté de participer », mais « les pays du <location id="ygkCmBH5r3">Golfe</location"> – <loc_ref_to_org id="JPe0jRFuW3">Koweït</loc_ref_to_org">, <loc_ref_to_org id="izCViwC_-3">Qatar</loc_ref_to_org">, <loc_ref_to_org id="xOdJ1tKUjD">Émirats arabes unis</loc_ref_to_org">, <loc_ref_to_org id="CuiC6YqpSP">Arabie saoudite</loc_ref_to_org"> – ont été invités », a ajouté l'<organization id="iB6gAyg5fK">Élysée</organization"> précisant n'avoir « aucun doute qu'ils seront représentés ». Les institutions européennes participeront aussi à cette conférence pour mobiliser une aide humanitaire d'urgence. Si l'<organization id="lj1X9ZnsBf">ONU</organization"> a évalué à 85 millions de dollars les besoins du <loc_ref_to_org id="iCdxdE8Pj7">Liban</loc_ref_to_org"> pour le seul secteur de la santé, l'entourage du président français n'a pas voulu donner le montant de l'aide qui pourrait être dégagée <rel_date id="b25-UuwxfT">dimanche</rel_date">.

##Résultat##

[{"central": ["-VmQodN2NL"], "associated": [["LGoaNSV59T"], ["cg4GoqZIU1"]]}]

#Exemple#

##Texte annoté en entités##

 letemps.ch La Britannique exposée au <toxic_c_agent id="0bnYa-mbuQ">Novitchok</toxic_c_agent"> est morte <doc_source id="-Ivao20m50">Le Temps</doc_source"> ~4 minutes  Publié le <doc_date id="zGDavrN90d">08 juillet 2018</doc_date"> à 05:52. / Modifié le <doc_date id="Wrxh4SCsWu">10 juin 2023</doc_date"> à 16:24. La Britannique contaminée à l’agent innervant <toxic_c_agent id="YI7r6WEn2x">Novitchok</toxic_c_agent"> est décédée <rel_date id="Bb6MzNl521">dimanche</rel_date"> soir à l’<org_ref_to_loc id="VQhZd2Djd6">hôpital de Salisbury</org_ref_to_loc"> (sud-ouest de l’<location id="dW1yuP3v7h">Angleterre</location">) où elle avait été admise <rel_date id="G2lGfhzJF5">il y a huit jours</rel_date">, a annoncé la <organization id="3Tz2ZECKEm">police</organization">. « La <organization id="g3QHHQPJRO">police</organization"> a ouvert une enquête pour meurtre après que la femme exposée à l’agent <toxic_c_agent id="MNGSheX9hS">Novitchok</toxic_c_agent"> à <location id="oU135Mwz-C">Amesbury</location">, dans le <location id="VYJ-_5s8By">Wiltshire</location">, est décédée », a annoncé <organization id="pRnuoB2UzC">Scotland Yard</organization">. La victime, âgée de 44 ans, était originaire de <location id="qg2BbSVKZw">Durrington</location">. La première ministre Theresa May a immédiatement réagi, se disant « horrifiée et choquée » dans un communiqué. « La <organization id="Sb_9RlvSAz">police</organization"> et les agents de sécurité travaillent pour établir les faits de manière urgente », a-t-elle ajouté. « Le <organization id="HYuRTz_jlV">gouvernement</organization"> apporte tout son soutien à la population locale, confrontée à cette tragédie. » Neil Basu, le chef de la <organization id="M9tNiTCdN1">police antiterroriste</organization">, en charge de l’investigation, a déclaré que « cette terrible nouvelle ne servira qu’à renforcer notre détermination à résoudre cette enquête, identifier et traduire en justice les responsables ». La victime « laisse derrière elle sa famille, ses trois enfants, nos pensées et nos prières sont pour eux dans cette période extrêmement difficile ». Lire aussi : A <location id="bpzonlLqYr">Salisbury</location">, l’agent innervant <toxic_c_agent id="nry8cWJr9k">Novitchok</toxic_c_agent"> a frappé au hasard L’homme de 45 ans – qui avait aussi été hospitalisé le <rel_date id="rphOomsnnW">30 juin</rel_date"> – est toujours dans un état critique, a précisé <organization id="xlUwsKUVRQ">Scotland Yard</organization">. Les deux quadragénaires avaient été hospitalisés après avoir manipulé un « objet contaminé», avait indiqué la <organization id="PsaIS-ZCNb">police</organization"> en <fuzzy_period id="Df1Ya4QNo_">fin de semaine</fuzzy_period">. Une des hypothèses est que « l’un des deux a ramassé le contenant utilisé pour stocker l’agent neurotoxique utilisé contre les Skripal », selon une source gouvernementale. La population inquiète Leur contamination est survenue <rel_date id="4DDbLZPYgR">quatre mois après la tentative d’empoisonnement</rel_date"> au <toxic_c_agent id="P-sACr2Df0">Novitchok</toxic_c_agent"> qui a visé l’ex-espion russe Sergueï Skripal et sa fille Ioulia à <location id="PnX-nn3COi">Salisbury</location">, une ville située à une dizaine de kilomètres seulement d’<location id="M1xj9cZ2Ut">Amesbury</location">, où les ambulances avaient pris en charge le couple de Britanniques. La police n’a pas pu établir si le <toxic_c_agent id="X8D9GlyVN-">Novitchok</toxic_c_agent"> provenait du même lot dans les deux cas. Ioulia et Sergueï Skripal avaient pu sortir de l’hôpital après <fuzzy_period id="3LEUWrTQ-Y">plusieurs semaines</fuzzy_period"> de soins, tout comme Nick Bailey, le premier policier qui leur avait porté secours. Ce dernier avait été hospitalisé dans un état grave. « Je sais que cette nouvelle va affecter beaucoup de monde, audelà de ceux qui connaissaient la victime », a dit Kier Pritchard, chef de la <organization id="MqC54ggfcC">police du comté de Wiltshire</organization">. Elle devrait aussi faire augmenter l’ « inquiétude» de la population, a-t-il ajouté. Les habitants de <location id="CXIzlUQME5">Salisbury</location"> et d’<location id="-U2e8IXqs_">Amesbury</location"> avaient déjà fait part de leurs craintes et de leur incompréhension après l’annonce de l’hospitalisation du couple et l’apparition de plusieurs cordons policiers dans les deux villes. Lire aussi : Mais qu’est-ce que le <toxic_c_agent id="o9WGQK8WdI">Novitchok</toxic_c_agent">, ce poison utilisé contre Sergueï Skripal? La tentative d’empoisonnement des Skripal avait été attribuée par <loc_ref_to_org id="oG8-nvtIng">Londres</loc_ref_to_org"> à <loc_ref_to_org id="y1NeCxP3u6">Moscou</loc_ref_to_org">, qui avait nié toute implication. L’affaire avait déclenché une grave crise diplomatique entre le <loc_ref_to_org id="X4e2X5Q73f">Kremlin</loc_ref_to_org"> et les Occidentaux et une vague d’expulsions croisées de diplomates. En visite à <location id="onL5lJe4gl">Salisbury</location"> <rel_date id="yhnIlw7Gup">dimanche</rel_date">, le ministre de l’Intérieur Sajid Javid a annoncé que le <organization id="63XL64gWks">gouvernement britannique</organization"> n’avait «pas pour projet actuel» d’imposer de nouvelles sanctions à la <loc_ref_to_org id="ZqYuCD3DlP">Russie</loc_ref_to_org">. Lire aussi: Les articles du Temps.ch sur l’affaire Skripal

##Résultat##

[{"central": ["P-sACr2Df0", "YI7r6WEn2x", "nry8cWJr9k", "X8D9GlyVN-", "MNGSheX9hS", "0bnYa-mbuQ", "o9WGQK8WdI"], "associated": [["zGDavrN90d", "Bb6MzNl521", "yhnIlw7Gup"], ["VQhZd2Djd6"], ["oU135Mwz-C", "M1xj9cZ2Ut", "-U2e8IXqs_"], ["PnX-nn3COi", "CXIzlUQME5", "onL5lJe4gl", "bpzonlLqYr"], ["4DDbLZPYgR"], ["G2lGfhzJF5", "rphOomsnnW"]]}]

#Exemple#

##Texte annoté en entités##

 Les rejets de <radioisotope id="tSeefq8NFm">césium 137</radioisotope"> à <location id="bLxfpz9QuR">Fukushima</location"> 168 fois plus importants qu'à <location id="oNVs_Xg__V">Hiroshima</location">  La quantité de <radioisotope id="plS430PbR1">césium radioactif</radioisotope"> dégagée <rel_period id="bBRpn3yqkX">depuis le 11 mars</rel_period"> par la <org_ref_to_loc id="VCcAuwiIXY">centrale nucléaire accidentée de Fukushima</org_ref_to_loc"> (nord-est du <location id="sqUuLn4U1A">Japon</location">) est 168 fois plus importante que celle dispersée en un instant par la bombe atomique d'<location id="Jrh5Kitcb9">Hiroshima</location">, a affirmé <rel_date id="OetScrQSIy">jeudi</rel_date"> un journal nippon. Selon le <organization id="p9g_R0zpty">Tokyo Shimbun</organization">, qui dit s'appuyer sur des estimations du gouvernement, les réacteurs endommagés par un tsunami géant ont dégagé jusqu'ici 15.000 terabecquerels de <radioisotope id="qQQkwKeWJY">césium 137</radioisotope"> au fil des mois. En <abs_period id="EcCJM7KHX0">août 1945</abs_period">, la bombe atomique larguée par l'<organization id="rq08Zn_PwH">armée américaine</organization"> au-dessus de la<location id="uqyqQaRUmN"> ville d'Hiroshima</location"> (sud-ouest) avait relâché instantanément dans l'atmosphère 89 terabecquerels de cet isotope dont la période radioactive est de 30 ans, a ajouté le journal. "En théorie, la quantité de <radioisotope id="5mdotT0Ur2">césium 137</radioisotope"> échappé de la <org_ref_to_loc id="e2-chZrZHY">centrale de Fukushima</org_ref_to_loc"> est donc 168,5 fois plus importante que celle de la bombe américaine", a-t-il souligné, en affirmant que cette estimation avait été calculée par le <organization id="DnlFBh-cqb">gouvernement</organization"> à la demande d'une commission du <organization id="wlZAm6i8V7">Parlement</organization">. Mais là s'arrête la comparaison, car la bombe A a fait 140.000 morts, tués immédiatement par la chaleur ou le souffle de l'explosion, ou dans les mois suivant à cause des effets des radiations, alors que l'accident de Fukushima n'a causé jusqu'ici aucun décès. Le gouvernement juge d'ailleurs "non rationnel" de comparer ainsi la contamination radioactive d'une centrale nucléaire avec celle d'une arme atomique destinée à tuer. La même comparaison révèlerait que l'explosion du réacteur de <org_ref_to_loc id="Q1LzH0jONp">Tchernobyl</org_ref_to_loc"> (<location id="WQJb2mfDhO">Ukraine</location">) en <abs_period id="DZnIroDFge">1986</abs_period"> a dispersé dans l'environnement 900 fois plus de <radioisotope id="yM5XbLIFMZ">césium 137</radioisotope"> que la bombe d'<location id="u24M5QbUmz">Hiroshima</location">, si l'on s'en réfère aux évaluations de l'<organization id="nqUacpnCx4">Institut français de la radioprotection et de la sûreté nucléaire</organization"> (<organization id="H9mST1kUk2">IRSN</organization">). Après l'éclatement de la crise nucléaire de la <organization id="fgqWenQrn1">centrale de Fukushima Daiichi</organization"> (exploitée par <organization id="TnWYcqz4F5">Tepco</organization">), la plus grave depuis celle de <location id="ZMP3y4wS_4">Tchernobyl</location">, les autorités japonaises ont décrété une zone d'évacuation obligatoire dans un rayon de 20 kilomètres autour site. Plus de 85.000 personnes vivent <fuzzy_period id="OqfI5mQFqv">depuis plus de cinq mois</fuzzy_period"> dans des centres d'accueil ou des logements préfabriqués, sans aucune certitude de retrouver un jour leur habitation.

##Résultat##

[{"central": ["qQQkwKeWJY", "tSeefq8NFm", "5mdotT0Ur2", "yM5XbLIFMZ"], "associated": [["bBRpn3yqkX"], ["VCcAuwiIXY", "e2-chZrZHY"]]}, {"central": ["Q1LzH0jONp", "ZMP3y4wS_4"], "associated": [["DZnIroDFge"], ["qQQkwKeWJY", "tSeefq8NFm", "5mdotT0Ur2", "yM5XbLIFMZ"]]}, {"central": ["qQQkwKeWJY", "tSeefq8NFm", "5mdotT0Ur2", "yM5XbLIFMZ"], "associated": [["EcCJM7KHX0"]]}]

#Exemple#

##Texte annoté en entités##

 Mort d'un étudiant qui avait fabriqué un engin explosif grâce à Internet  La <organization id="5dQcmXKe4e">division de lutte contre la cybercriminalité de la gendarmerie</organization"> a été chargée d'enquêter, <rel_date id="QXEAKV1oVZ">vendredi 8 février</rel_date">, sur le ou les sites Internet qui ont aidé quatre jeunes hommes de l'<location id="_ScOk3a8cU">Oise</location"> à fabriquer des engins explosifs artisanaux. L'un d'entre eux est mort <rel_date id="tbnhhKNryA">jeudi</rel_date"> après que l'un de ces engins a explosé accidentellement. Dan Thibout, 21 ans, étudiant en informatique, se trouvait dans la cave du domicile familial à <location id="cba5e-be7N">Lamorlaye</location"> (<location id="oICyTZPUhL">Oise</location">) quand il a voulu perforer le tube rempli de désherbant et de sucre qu'il "bricolait". Selon les premiers éléments de l'enquête, confiée à la <organization id="rDTg8bNzeT">gendarmerie de Chantilly</organization">, c'est le blast de l'explosion qui l'aurait tué. Son frère, son cousin et un ami ont été légèrement blessés. Placés en garde à vue puis libérés, ils ont déclaré qu'ils voulaient refaire, en un peu plus gros, le feu d'artifice que la famille avait acheté pour la <rel_date id="PSyOOy4mwA">Saint Sylvestre</rel_date">. La nature de ces explosifs, et l'absence de toute documentation, ont permis aux gendarmes de <loc_ref_to_org id="IPyIp3i7Fm">Chantilly</loc_ref_to_org"> d'écarter la piste des mystérieux destructeurs de radars routiers actifs dans la région. Les trois jeunes hommes, âgés de 18 à 21 ans, sont passibles de poursuites pour fabrication de substances explosives, indique Etienne Laguarigue de Survilliers, substitut du procureur. Mais l'enquête sur les sites Internet risque de se révéler délicate. A supposer que la <organization id="CLf4HjLi99">division cybercriminalité</organization">, associée à la <organization id="sUxkZZIAoF">brigade départementale de renseignement et d'investigation judiciaire</organization"> (<organization id="dpafLmY9Jl">BDRIJ</organization">), remonte jusqu'à une adresse IP lui permettant d'identifier les ordinateurs des sites concernés, bien souvent la quête aboutit à l'étranger. En <location id="BCojhZ_huZ">France</location">, le code pénal prévoit une peine de trois ans d'emprisonnement et 45 000 euros d'amende pour diffusion à un public non professionnel de fabrication d'engins explosifs. Cette peine est aggravée, cinq ans d'emprisonnement et 75 000 euros, si cette diffusion passe par Internet. <doc_author id="3_MbkxclLu">Isabelle Mandraud</doc_author">

##Résultat##

[]

#Exemple#

##Texte annoté en entités##

 Quatre suspects ont fui la <location id="g5Mkaq1mOS">Malaisie</location"> le <rel_date id="bIuUgiV9Ib">jour de l'assassinat</rel_date"> Mort de Kim JongNam: le <toxic_c_agent id="YaGcuUsZf1">VX</toxic_c_agent"> a paralysé la victime, dit <loc_ref_to_org id="jxqJBImNck">Kuala Lumpur</loc_ref_to_org"> Publié le <doc_date id="YFoA8BAyrw">26 février 2017</doc_date"> à 13:31  Le demi-frère du numéro un nord-coréen a succombé à une paralysie causée par un puissant agent neurotoxique, selon les résultats d'autopsie révélés <rel_date id="xALpWJ1mOp">dimanche</rel_date"> par le ministre malaisien de la Santé tandis que l'<org_ref_to_loc id="2LbRC3Wy0I">aéroport de Kuala Lumpur</org_ref_to_loc">, théâtre de son assassinat, était déclaré exempt de tout danger. La <loc_ref_to_org id="FDpALitQFM">Malaisie</loc_ref_to_org"> a révélé <rel_date id="KuGQAhSS9U">vendredi</rel_date"> que le meurtre le <rel_date id="t0Mk_zCAJR">13 février</rel_date"> de Kim Jong-Nam, demi-frère de Kim Jong-Un, avait été perpétré avec du <toxic_c_agent id="BVSKafaX6d">VX</toxic_c_agent">, un agent neurotoxique classé comme arme de destruction massive, dans un scénario digne d'un roman d'espionnage. Les résultats de l'autopsie suggèrent que la victime âgée de 45 ans a succombé à une "paralysie très grave" et est décédée dans "un très court laps de temps", a déclaré le ministre S. Subramaniam. Deux femmes soupçonnées d'avoir administré la substance ont été placées en détention provisoire, de même qu'un Nord-Coréen. La police veut entendre sept autres Nord-Coréens -- dont un diplomate de l'<organization id="wiCeRiHxnu">ambassade de Corée du Nord à Kuala Lumpur</organization"> -- mais quatre des suspects ont fui la <location id="Lo-7Zj0yCK">Malaisie</location"> le <rel_date id="oZwueMDaDD">jour de l'assassinat</rel_date">. Sur des images de vidéo-surveillance qui ont fuité dans les médias, on peut voir Kim Jong-Nam approché de dos par deux femmes dont l'une lui projette apparemment quelque chose au visage. La victime avait ensuite été conduite à la <org_ref_to_loc id="30tSvfd4kH">clinique de l'aéroport</org_ref_to_loc"> avant de succomber pendant son transfert à l'hôpital. Les deux suspectes affirment qu'elles ont été dupées bien que la <organization id="FpDSLIuBgO">police malaisienne</organization"> assure qu'elles savaient ce qu'elles faisaient. Le <toxic_c_agent id="Un9D2jO5fA">VX</toxic_c_agent"> est une version plus mortelle du <toxic_c_agent id="BBNtcNPM4v">gaz sarin</toxic_c_agent">, indolore, inodore et hautement toxique. Les agents neurotoxiques stimulent excessivement les glandes et muscles, ce qui les fatigue rapidement et attaque la respiration. D'après M. Subramaniam, les causes de la mort sont désormais "plus ou moins confirmées". Pendant toute la nuit, les personnels de la <organization id="mgTwue51_R">défense civile</organization"> vêtus de combinaisons de protection blanches ont passé au crible la scène du crime. Les autorités ont ensuite déclaré n'avoir rien trouvé et que l'aéroport était sûr. - L'enquête continue - La police avait établi un cordon de sécurité dans une grande partie du <location id="FzTWnng-JD">hall des départs du terminal 2</location"> sous les regards des curieux. "La police a bouclé trois zones: la scène de l'attaque, les toilettes où les deux suspectes se sont lavé les mains et le chemin emprunté pour aller à la <org_ref_to_loc id="ycIbxnUi5g">clinique de l'aéroport</org_ref_to_loc">", selon un porte-parole. Cette opération menée <rel_date id="5_NKo9LP_J">près de deux semaines après l'assassinat</rel_date"> en a surpris plus d'un. "Je suis un peu inquiet", a déclaré à l'<organization id="PUrwzoNw9P">AFP</organization"> Hariz Syafiq, étudiant de 21 ans en attendant son vol. "Pourquoi n'ont-ils pas placé l'aéroport sous quarantaine? C'est un peu étrange". L'une des suspectes, Siti Aisyah, une Indonésienne de 25 ans, a raconté avoir reçu l'équivalent de 90 dollars pour prendre part à ce qu'elle pensait être une émission de télévision type caméra cachée, selon un haut diplomate cité par les médias. Elle pensait manipuler de "l'huile pour bébé". Elle ne connaissait pas l'autre suspecte, selon la même source. Doan Thi Huong, Vietnamienne de 28 ans, a raconté aux autorités vietnamiennes avoir été piégée et qu'elle pensait elle aussi participer à un vidéo gag. La police a déclaré que l'une des suspectes était tombée malade après son arrestation, et avait été prise de vomissements. Abdul Samah Mat, chef de la <organization id="Sby7FmplIX">police de l'Etat de Selangor</organization">, où est situé l'aéroport, a expliqué à la presse que l'enquête se poursuivait dans un complexe résidentiel de <location id="bgvQxqmdkJ">Kuala Lumpur</location">, en lien avec les quatre Nord-Coréens ayant fui la <location id="RZVWw5s0pR">Malaisie</location"> le jour du meurtre. Des prélèvements ont été effectués sur les lieux aux fins d'analyses chimiques. L'annonce de l'emploi du <toxic_c_agent id="hSQ91n4TWR">VX</toxic_c_agent"> a semé la colère en <location id="fBdFuN-N6s">Malaisie</location">. La <loc_ref_to_org id="sd4OsAK7vy">Corée du Sud</loc_ref_to_org">, qui depuis le début de cette affaire pointe un doigt accusateur sur son <loc_ref_to_org id="J99KpOkrLu">voisin du Nord</loc_ref_to_org">, a dénoncé une "violation patente de la Convention sur les armes chimiques". <rel_date id="VK_A-OR2bh">Jeudi</rel_date">, <loc_ref_to_org id="OdST-6gwAu">Pyongyang</loc_ref_to_org"> a rompu le silence qu'il conservait depuis l'assassinat en tirant à boulets rouges sur la <loc_ref_to_org id="hwy_1669ZT">Malaisie</loc_ref_to_org">, accusée d'être responsable du décès et de comploter avec la <loc_ref_to_org id="85fa16Yuo4">Corée du Sud</loc_ref_to_org">.

##Résultat##

[{"central": ["Un9D2jO5fA", "YaGcuUsZf1", "hSQ91n4TWR", "BVSKafaX6d"], "associated": [["oZwueMDaDD", "bIuUgiV9Ib", "t0Mk_zCAJR"], ["30tSvfd4kH", "ycIbxnUi5g"], ["FzTWnng-JD"]]}]

#Exemple#

##Texte annoté en entités##

 Nouveaux cas d'<inf_disease id="yPCPzvJ90u">Ebola</inf_disease"> en <location id="mHUAriiz_u">Guinée</location"> - réouverture en urgence d'un centre de traitement <doc_date id="-o_wvYOMIY">18/03/2016</doc_date"> &&  <doc_source id="YfxBH6PFYv">AFP</doc_source">      Il s'agit d'une mère et de son fils de cinq ans, selon l'<organization id="22Cyq_uOsR">OMS</organization">. L'organisation <organization id="MwggiPbG2m">Alima</organization"> a rouvert en urgence le <org_ref_to_loc id="lQ1mZgG9mY">centre de traitement Ebola de N'Zérékoré</org_ref_to_loc">, en <location id="oMnAkiabVX">Guinée forestière</location">. Deux malades d'<inf_disease id="gBCOcXQYTx">Ebola</inf_disease"> identifiés dans le sud de la <location id="0ZrG2xeBYf">Guinée</location"> après le décès de deux membres de leur famille atteints par le virus ont été admis dans un centre de traitement, a annoncé <rel_date id="05w4TB5wL5">vendredi</rel_date"> l'ONG <organization id="jvLVKMiMJU">Alima</organization">, qui les a pris en charge. Il s'agit d'"une mère et de son fils de 5 ans", a indiqué de son côté l'<organization id="5saH9R5wDM">Organisation mondiale de la Santé</organization"> (<organization id="97rszypdoz">OMS</organization">) dans un communiqué, précisant avoir été alertée sur une possible résurgence d'<inf_disease id="NsPFm-fxKo">Ebola</inf_disease"> en <location id="zpfTH8mqIj">Guinée</location"> <rel_period id="HHQnGd_R04">depuis le 16 mars</rel_period">, à la suite de décès inexpliqués dans une famille présentant des symptômes du virus. Les équipes dépêchées sur place par l'<organization id="NP4q57AELw">OMS</organization"> et le <organization id="u2RyTI1Opq">ministère de la Santé</organization"> "s'efforceront d'enquêter sur l'origine des nouvelles contaminations et d'identifier, isoler, vacciner et surveiller tous les contacts des nouveaux cas et des morts", ajoute l'organisation. Selon un communiqué d'<organization id="m2cUpRWeG5">Alima</organization">, "deux patients confirmés <inf_disease id="V4nuIkQV93">Ebola</inf_disease"> ont été pris en charge par l'organisation <organization id="sfVpM84Vpx">Alima</organization"> (<organization id="ocf316JOS9">The Alliance For International Medical Action</organization">) qui a rouvert en urgence le <org_ref_to_loc id="PvzbHRNB2q">centre de traitement Ebola de N'Zérékoré</org_ref_to_loc">, en <location id="KdAgBCYpSH">Guinée forestière</location">", à une centaine de kilomètres de <location id="QusZHU6KTj">Koropara</location">, où les nouveaux cas ont été signalés. "Nous espérons que ce nouveau foyer sera très vite circonscrit car aujourd'hui les autorités et les communautés se sont approprié les bonnes pratiques pour lutter contre la maladie", a dit le président d'<organization id="JO1wmGwVvT">Alima</organization">, Richard Kojan, présent en <location id="jwXIvdrK2b">Guinée</location">, cité dans le texte. L'<organization id="E97dSUbjHU">ONG</organization">, qui a participé à l'expérimentation d'un traitement antiviral japonais prometteur contre <inf_disease id="uyvkBVZNzR">Ebola</inf_disease">, assure en <location id="QKbxso3crf">Guinée</location"> "des soins médicaux et un soutien psycho-social à près de 115 patients guéris". Le <pathogen id="XRemhh04tp">virus Ebola</pathogen"> a été identifié sur deux personnes d'une même famille décédées dans le sud-est de la <location id="07gA2qALNG">Guinée</location">, ainsi qu'au moins deux de leurs proches, les deux premiers cas signalés dans ce pays depuis que la fin de l'épidémie y a été proclamée le <rel_date id="VrDgElhkDA">29 décembre</rel_date">, a annoncé <rel_date id="eFP4d60NNT">jeudi</rel_date"> le <organization id="EkdOUZcMUl">gouvernement</organization">. Une source proche de la <organization id="kooXWHJO_z">Coordination locale de lutte contre Ebola</organization"> a précisé à l'<organization id="Ic1Io5Eql0">AFP</organization"> sous le couvert de l'anonymat que les deux personnes décédées étaient un couple marié. <rel_date id="rX2_4wADVr">Jeudi</rel_date"> matin, l'<organization id="7MejjlXK8r">OMS</organization"> avait pourtant annoncé l'arrêt présumé de "toutes les chaînes de transmission initiales" de l'épidémie en <location id="u1RWxiHdKj">Afrique de l'Ouest</location"> après la fin du dernier épisode de la maladie en <location id="HTCafClZht">Sierra Leone</location"> voisine.

##Résultat##

[{"central": ["PvzbHRNB2q", "lQ1mZgG9mY"], "associated": [["V4nuIkQV93", "gBCOcXQYTx", "uyvkBVZNzR", "yPCPzvJ90u", "NsPFm-fxKo"], ["HHQnGd_R04"], ["QusZHU6KTj"]]}, {"central": ["V4nuIkQV93", "gBCOcXQYTx", "uyvkBVZNzR", "yPCPzvJ90u", "NsPFm-fxKo"], "associated": [["07gA2qALNG", "QKbxso3crf", "0ZrG2xeBYf", "mHUAriiz_u", "jwXIvdrK2b", "zpfTH8mqIj"], ["VrDgElhkDA"]]}, {"central": ["V4nuIkQV93", "gBCOcXQYTx", "uyvkBVZNzR", "yPCPzvJ90u", "NsPFm-fxKo"], "associated": [["eFP4d60NNT", "rX2_4wADVr"], ["u1RWxiHdKj"]]}]

#Exemple#

##Texte annoté en entités##

 © Photo  <organization id="VjL3LcBwHA">Sanofi</organization"> renonce à développer un vaccin anti-Zika <doc_date id="E5AangJPMT">07/09/2017</doc_date"> &&  Communiqué de presse  Le géant pharmaceutique français <organization id="lp6eqH8m5P">Sanofi</organization"> a abandonné son programme de développement d'un vaccin contre le virus Zika, après qu'une autorité américaine a décidé de réduire ses financements en raison du déclin de l'épidémie. Il y a un an, <organization id="EBRTxCefJd">Sanofi</organization"> avait obtenu un engagement de 43,2 millions de dollars de la part de l'<organization id="qGmViXdON3">Autorité américaine de recherche et développement avancés dans le domaine biomédical</organization"> (<organization id="JOFjEA4a5E">BARDA</organization">), pour financer le développement d'un vaccin anti-Zika. Cependant le <rel_period id="x-DCfE8526">mois dernier</rel_period">, cette institution a décidé de réduire drastiquement le périmètre de son accord avec <organization id="cHLDRKUff5">Sanofi Pasteur</organization">, la division vaccins du groupe, selon une déclaration de <organization id="s93zLxXjor">Sanofi</organization"> discrètement publiée sur son site américain <fuzzy_period id="LiG9vgZRU2">début septembre</fuzzy_period">. "Par conséquent, <organization id="YpzOHZ_2T4">Sanofi</organization"> n'a pas l'intention de continuer à développer un candidat-vaccin contre Zika pour le moment", ni d'obtenir une licence sur une technologie de l'<organization id="IZrFSrUpBe">institut de recherche Walter Reed Army</organization">, que ce vaccin devait utiliser, a ajouté <organization id="A2u57ojnkr">Sanofi</organization">. Son développement risquait par ailleurs de prendre bien plus de temps et de moyens que prévu. <organization id="lzfidYIrKs">Sanofi</organization"> "respecte la décision de la <organization id="MpcuSrcYxW">BARDA</organization"> de réallouer ses ressources limitées vers ses priorités", sur fond d'une "forte réduction du nombre de nouveaux cas de <inf_disease id="dPbwngMQtX">Zika</inf_disease"> aux <location id="fIHKvH4ZXv">Etats-Unis</location"> et dans le <location id="7sq2hLCF8e">monde</location"> en <abs_period id="l-V2j06WkV">2017</abs_period">", a encore commenté le groupe. L'<organization id="IJikmmBiZq">Organisation mondiale de la santé</organization"> (<organization id="OH6lmp7vCS">OMS</organization">) avait retiré en <rel_period id="v1xQ_v5iAs">novembre dernier</rel_period"> le statut d'"urgence de santé publique de portée mondiale" du <pathogen id="ywuK27sBP4">virus Zika</pathogen">, lié à de graves anomalies cérébrales chez les nourrissons et touchant majoritairement des pays d'<location id="XBmDmoWFMi">Amérique latine</location">. Plusieurs dizaines de vaccins contre le Zika sont actuellement à l'étude, mais aucun ne sera disponible pour les femmes en âge de procréer avant <abs_period id="0BqjoETegr">2020</abs_period">, avait estimé ultérieurement l'<organization id="jwSbB7qulX">OMS</organization">. <organization id="4fJrzI2ggK">Sanofi</organization"> va limiter sa collaboration avec la <organization id="G7UbFiCxNh">BARDA</organization"> à une étude de cas et de surveillance épidémiologique du <inf_disease id="awgrxnELa0">Zika</inf_disease"> sur 2.400 volontaires en <location id="rCsbRP7n68">Colombie</location">, au <location id="51nism0Wsq">Honduras</location">, au <location id="BBSTZh_CyS">Mexique</location"> et à <location id="S4ZV0lnj1P">Puerto Rico</location">, a précisé le groupe dans sa déclaration.

##Résultat##

[{"central": ["awgrxnELa0", "dPbwngMQtX"], "associated": [["7sq2hLCF8e"], ["l-V2j06WkV"], ["ywuK27sBP4"]]}]

#Exemple#

##Texte annoté en entités##

 Un disparu, douze blessés et des milliers d’évacués après l’explosion d’un dépôt de munitions en <location id="ljjcMRvrjo">Sibérie</location">  L’explosion survenue <rel_date id="jMvivXfSnU">lundi 5 août</rel_date"> dans un dépôt militaire en <location id="YeOuEjNH_l">Sibérie</location"> a rendu nécessaires de nombreuses évacuations. DMITRY DUB / <organization id="cGmJ-TsVlf">AP</organization"> Les débris ont volé à plusieurs kilomètres alentour. Une personne est portée disparue, douze ont été blessées et des milliers de personnes évacuées, <rel_date id="i2TUARn61u">lundi 5 août</rel_date">, à la suite d’explosions causées par un incendie dans un dépôt de munitions en <location id="9-vJiyIjVN">Sibérie</location">. D’après des médecins, sept personnes ont été blessées, et deux d’entre elles ont été hospitalisées, a rapporté l’agence publique <organization id="GHByKuIhDm">TASS</organization">. Provoquée par un feu d’origine inconnue, l’explosion principale s’est produite vers 17 heures, heure locale. Il a pris dans un dépôt d’obus d’une unité militaire stationnée près du <location id="A5jnIcFIuM">village de Kamenka</location">, a précisé le communiqué publié sur le site officiel du gouverneur de la <location id="KGnzw4EYhk">région de Krasnoïarsk</location">. D’après les autorités locales, 9 500 habitants ont été évacués dans un rayon de 15 kilomètres autour de la catastrophe. L’état d’urgence a été décrété. Des témoins ont publié sur Internet des vidéos montrant une épaisse fumée noire s’élevant au-dessus d’une forêt située à côté du dépôt de munitions. Le quotidien britannique <organization id="qOLKsVCUE4">The Guardian</organization"> a publié sur site une vidéo montrant l’explosion : « Les munitions continuent d’exploser depuis déjà cinq heures. Plusieurs milliers ont explosé », a déclaré une source aux services de secours locaux, citée par l’agence <organization id="36W4-ivpNM">TASS</organization">. Plusieurs trains équipés pour la lutte antiincendie ont été dépêchés sur les lieux. « Des mesures ont été prises pour empêcher la propagation du feu et assurer la sécurité » dans la zone des explosions, a fait savoir l’antenne locale du <organization id="umsGbFFohB">ministère des situations d’urgence russe</organization">. <doc_source id="vyozpQ3_6L">Le Monde</doc_source"> avec <doc_source id="qkKIHWEOdC">AFP</doc_source">

##Résultat##

[]

#Exemple#

##Texte annoté en entités##

 <inf_disease id="6wxkukowDP">Zika</inf_disease"> - <loc_ref_to_org id="dnHi2ZdrOW">Porto Rico</loc_ref_to_org"> décrète l'état d'urgence sanitaire, une femme enceinte infectée  Publié le <doc_date id="Zgz0yP0VMk">05/02/2016</doc_date"> à 08h01   Le gouverneur de <loc_ref_to_org id="bq3q33eR6K">Porto Rico</loc_ref_to_org">, Alejandro Garcia Padilla, a décrété l'état d'urgence sanitaire <rel_date id="paa6UdQYXE">vendredi</rel_date"> dans l'île des <location id="tN9JMek-L8">Caraïbes</location"> où 22 personnes ont été infectées par le <pathogen id="Atwmo9GRn6">virus Zika</pathogen">, dont une femme enceinte. "Notre objectif principal est d'assurer la sécurité des Porto-ricains et de leur donner des conseils sur les mesures préventives nécessaires", a déclaré M. Garcia Padilla dans un discours depuis le <location id="fM1QLiGTzT">palais présidentiel</location">. Des responsables ont précisé que dans le cadre de ce plan d'urgence, l'accent allait être mis sur la lutte contre les moustiques, principaux vecteurs du virus. D'autres mesures vont également entrer en vigueur, comme le gel des prix de certains produits -les préservatifs par exemple- une mesure prise après un cas confirmé de transmission du virus par voie sexuelle aux <location id="l1-vjRxddr">Etats-Unis</location">. "Le <inf_disease id="kDziHgb9vv">Zika</inf_disease"> doit être traité comme une <inf_disease id="P8k4uoFVse">maladie sexuellement transmissible</inf_disease">, nous devons prendre les précautions adéquates", a dit Ana Rius, secrétaire à la Santé de l'île des <location id="2Pu_RVkbkT">Caraïbes</location">. Trois nouveaux cas de <inf_disease id="T4vCPli0tw">Zika</inf_disease"> ont été répertoriés dans l'archipel américain de <location id="snsMZcPRGe">Porto Rico</location">, ce qui porte le nombre total de personnes infectées à 22, selon les autorités. Parmi ces patients figure une femme enceinte. Mme Rius, qui avait déjà conseillé aux femmes le <rel_period id="ysblrDkH5n">mois dernier</rel_period"> d'éviter de tomber enceintes, a aussi annoncé qu'une période de quarantaine avait été établie pour les dons du sang. Les autorités de santé américaines ont recommandé plus tôt <rel_date id="y1e1hYEBxi">vendredi</rel_date"> aux personnes de retour de pays où sévit le <pathogen id="HZ6Psff_XY">virus Zika</pathogen"> d'utiliser des préservatifs ou de s'abstenir d'avoir des relations sexuelles, le virus pouvant se transmettre par cette voie. Bénigne en apparence, l'infection par ce virus est soupçonnée de provoquer de graves malformations congénitales du cerveau du foetus chez les femmes enceintes. L'<organization id="WG2TjOMdCm">organisation mondiale de la santé</organization"> (<organization id="BBBeAX6xfC">OMS</organization">) a qualifié l'épidémie d'"urgence de santé publique de portée mondiale".

##Résultat##

[{"central": ["6wxkukowDP", "T4vCPli0tw", "kDziHgb9vv"], "associated": [["HZ6Psff_XY", "Atwmo9GRn6"], ["snsMZcPRGe"], ["y1e1hYEBxi", "paa6UdQYXE", "Zgz0yP0VMk"]]}]

#Exemple#

##Texte annoté en entités##

 <location id="Vs4ZgZKYmG">RHÔNE</location"> <location id="IWMr-sXLP0">Lyon 8e</location"> : 500 grammes d’un puissant explosif découverts dans un square 500 grammes d’un puissant explosif, le <explosive id="YOsiFxkolW">Semtex</explosive">, ont été découverts <rel_date id="aGOSLPadu1">jeudi</rel_date"> après-midi dans le <location id="uoCN2OftmD">quartier Mermoz</location">, lors d’une opération initialement menée sur de la recherche de produits stupéfiants. La saisie a été effectuée dans un jardin public. <doc_source id="nZSFljaKIi">Le Progrès</doc_source"> - <doc_date id="jPXdKljER7">04 déc. 2015</doc_date"> à 10:32 | mis à jour le <doc_date id="yKDANmfts4">05 déc. 2015</doc_date"> à 14:14 - Temps de lecture : 1 min La marchandise avait été dissimulée dans la souche d’un arbre, vraisemblablement pour que ses propriétaires puissent se soustraire aux risques des perquisitions menées dans le cadre de l’état d’urgence. Selon une source proche du dossier, cette découverte n’a pas de lien avec la piste terroriste, mais celle du grand banditisme. Le <explosive id="ljunxSVg1G">semtex</explosive"> a déjà été utilisé, dans la région, pour faire sauter des distributeurs automatiques de billets. L’enquête a d’ailleurs été confiée à la <organization id="SjWoaLWX0N">Police Judiciaire de Lyon</organization">. La même substance dérobée en <abs_period id="KScBfES8Kz">2008</abs_period"> au <location id="-E55iOsHDC">fort de Corbas</location"> Le <explosive id="DGVHUhITUx">Semtex</explosive"> est un puissant explosif très polyvalent : utilisé tant dans le domaine industriel pour la démolition, que dans l’armée pour produire des mines, il est aussi très prisé par les terroristes car son absence d’odeur le rend très difficile à détecter. En <abs_period id="YpPl-aS5tg">2008</abs_period">, 28 kilos de cette substance avaient été dérobés au <location id="bgTCTW-zKj">fort de Corbas</location"> suite à une négligence de sécurité. Le butin de ce vol retentissant n’a jamais été retrouvé. Il est encore trop tôt pour savoir si la découverte d’<rel_date id="CTkHcY_OsL">hier</rel_date"> en fait partie.

##Résultat##

[{"central": ["YOsiFxkolW", "ljunxSVg1G", "DGVHUhITUx"], "associated": [["CTkHcY_OsL", "aGOSLPadu1"], ["uoCN2OftmD"]]}, {"central": ["YOsiFxkolW", "ljunxSVg1G", "DGVHUhITUx"], "associated": [["YpPl-aS5tg", "KScBfES8Kz"], ["-E55iOsHDC", "bgTCTW-zKj"]]}]

#Exemple#

##Texte annoté en entités##

 <location id="A_H6LrUp_6">Allemagne</location">: un Iranien soupçonné de préparer un attentat "islamiste" au <toxic_c_agent id="MRBXUgNdzt">cyanure</toxic_c_agent"> et à la <bio_toxin id="mgfaaAlCab">ricine</bio_toxin"> arrêté <doc_author id="3EjNvjuMG6">J.D.</doc_author"> avec <doc_source id="lTP8WtJad5">AFP</doc_source"> Le <doc_date id="Iz3Yx1d0UQ">08/01/2023</doc_date"> à 08h18 - mis à jour le <doc_date id="RI-U5To6Tz">08/01/2023</doc_date"> à 18h32 Des policiers en <location id="BK8Oj7wqML">Allemagne</location"> (photo d'illustration). - Christof Stache - <organization id="GIA3-E9d5c">AFP</organization"> L'homme de 32 ans a été interpellé, ainsi qu'une autre personne, dans l'ouest de l'<location id="21P8U2CxmX">Allemagne</location">. Il est "soupçonné d'avoir préparé un acte de violence grave menaçant la sûreté de l'État". Les autorités allemandes ont annoncé ce <rel_date id="cGobxv-D0V">dimanche</rel_date"> avoir interpellé un Iranien de 32 ans à la suite d'indications sur un possible attentat "islamiste" à la <bio_toxin id="DECY2Fz3gE">ricine</bio_toxin"> et au <toxic_c_agent id="wDwL7FTsS4">cyanure</toxic_c_agent">, suite à une mise en garde du <organization id="bQa4rk1KXL">FBI</organization"> selon la presse. L'appartement situé à <location id="ZXHfKfvIpr">Castrop-Rauxel</location"> dans l'ouest du pays, en <location id="SkfEemqhwo">Rhénanie du nord-Westphalie</location">, a été perquisitionné dans la nuit en vue de vérifier l'éventuelle présence de ces "substances toxiques" destinées à commettre une telle attaque, selon un communiqué du <organization id="nRR4qiZjo6">parquet régional</organization"> et de la <organization id="-JlqQjKb1e">police</organization">. Les enquêteurs n'ont cependant trouvé "aucun indice" sur la présence de ces produits sur place, a indiqué à l'<organization id="HhLE8nhZxh">AFP</organization"> le procureur de <loc_ref_to_org id="d3yfavXCk_">Düsseldorf</loc_ref_to_org">, Holger Heming. Alerte du <organization id="6nYSA3b_fV">FBI</organization"> Le ministre régional de l'Intérieur, Herbert Reul, a expliqué que les autorités avaient reçu "des indications à prendre au sérieux" qui ont conduit la <organization id="QOL6dHZM0X">police</organization"> à "agir durant la nuit". Selon les journaux <organization id="SWPvlyxkgP">Spiegel</organization"> et <organization id="70F00kBBLl">Süddeutsche Zeitung</organization">, c'est le <organization id="i9GOD8_-PO">FBI</organization"> américain qui a mis en garde les services allemands durant la <fuzzy_period id="ym9aSr-Awe">période de Noël</fuzzy_period">. La <organization id="6av2meOA4Y">police fédérale américaine</organization"> aurait réussi à infiltrer un groupe de la messagerie <organization id="DSIgYSHeF2">Telegram</organization">, où le suspect se serait renseigné d'abord sur des attentats à la bombe puis sur ceux commis à l'aide de substance toxiques, selon <organization id="5v5U0VAhAE">Der Spiegel</organization">. Le frère du suspect interpellé L'homme, en compagnie d'une deuxième personne également interpellée dans la nuit au même endroit, et qui selon les médias allemands est son frère, auraient envisagé de passer à l'action la nuit de la <rel_date id="_mNYO-6TA4">Saint-Sylvestre</rel_date">, mais il leur manquait des éléments pour la confection des poisons à la <bio_toxin id="QJ7VUGIxkP">ricine</bio_toxin"> et au <toxic_c_agent id="UPjX3fyB43">cyanure</toxic_c_agent">, ajoute le <organization id="GxvSYPX3jC">Spiegel</organization">. Malgré l'absence d'éléments à charge découverts immédiatement, la ministre fédérale de l'Intérieur, Nancy Faeser, a justifié le raid de la <organization id="eg7DI-homc">police</organization">. "Nos services de sécurité prennent chaque indice portant sur le danger du terrorisme islamiste très au sérieux", a-t-elle dit dans un communiqué. Reste à savoir maintenant si la justice aura suffisamment d'éléments pour engager des procédures. À ce stade, le principal suspect reste encore "soupçonné d'avoir préparé un acte de violence grave menaçant la sûreté de l'<organization id="leAvrl_ehR">État</organization"> en se procurant du <toxic_c_agent id="4tZqxUmel2">cyanure</toxic_c_agent"> et de la <bio_toxin id="8EQwxdU2I1">ricine</bio_toxin"> en vue de commettre un attentat à caractère islamiste", selon le communiqué publié par la justice locale. Sympathisant de l'<organization id="PAxjD35wKB">EI</organization"> Selon le <organization id="freRVPPH8t">Spiegel</organization">, l'homme est un Iranien sunnite sympathisant du groupe <organization id="dTwA22zpQi">État islamique</organization"> (<organization id="eqiO0zdmSP">EI</organization">). La <bio_toxin id="6ibWvM0618">ricine</bio_toxin"> est un agent très toxique classé par l'<organization id="ya8ELgzQTY">Institut Robert Koch</organization">, chargé en <location id="CuRJNQ4Opg">Allemagne</location"> de la veille médicale et sanitaire, comme "arme biologique" et est extraite de graines de la plante de ricine. Elle peut constituer un poison mortel, à l'instar du <toxic_c_agent id="F5lnaDf9xV">cyanure</toxic_c_agent">. Sur les images de la chaîne de télévision privée <organization id="raqY23YT0b">NTV</organization">, on voit les deux personnes interpellées emmenées en sous-vêtements par des agents, vêtus eux de combinaison de protection spéciale en raison du risque biologique. Un projet d'attentat à la <bio_toxin id="JzW9cTivpV">ricine</bio_toxin"> déjoué en <abs_period id="4tXRqaLsmX">2018</abs_period"> En <abs_period id="6VIVMJcsCh">2018</abs_period">, la <organization id="_MgGZYEadX">police allemande</organization"> avait déjà arrêté un Tunisien de 31 ans et son épouse, soupçonnés d'avoir voulu préparer ce qui aurait été le premier attentat "biologique" dans le pays. Chez le couple, qui avait prêté allégeance au groupe <organization id="YKubhWubtP">État islamique</organization">, les enquêteurs avaient retrouvé 84,3 mg de <bio_toxin id="f3EMtKspRM">ricine</bio_toxin"> et quelque 3300 graines de ricin permettant de fabriquer le poison. L'homme a été condamné deux ans plus tard à 10 ans de prison et sa femme à 8 ans d'emprisonnement. L'<location id="2IIyLXBgVW">Allemagne</location"> a été visée ces dernières années par plusieurs attaques islamistes, dont un attentat au camion-bélier sur un marché de Noël en <abs_period id="b5JgppDYz0">décembre 2016</abs_period"> qui avait fait 13 morts.

##Résultat##

[{"central": ["UPjX3fyB43", "F5lnaDf9xV", "4tZqxUmel2", "MRBXUgNdzt", "wDwL7FTsS4"], "associated": [["ZXHfKfvIpr"], ["RI-U5To6Tz", "Iz3Yx1d0UQ", "cGobxv-D0V"]]}, {"central": ["f3EMtKspRM", "DECY2Fz3gE", "6ibWvM0618", "mgfaaAlCab", "QJ7VUGIxkP", "8EQwxdU2I1", "JzW9cTivpV"], "associated": [["ZXHfKfvIpr"], ["RI-U5To6Tz", "Iz3Yx1d0UQ", "cGobxv-D0V"]]}, {"central": ["f3EMtKspRM", "DECY2Fz3gE", "6ibWvM0618", "mgfaaAlCab", "QJ7VUGIxkP", "8EQwxdU2I1", "JzW9cTivpV"], "associated": [["6VIVMJcsCh", "4tXRqaLsmX"], ["21P8U2CxmX", "2IIyLXBgVW", "BK8Oj7wqML", "CuRJNQ4Opg", "A_H6LrUp_6"]]}]

#Exemple#

##Texte annoté en entités##

 <location id="6E06_QqXdM">Kenya</location"> : la farine de maïs susceptible d'être infectée par une substance cancérigène Author, <doc_author id="h8L-32enmj">Basillioh Mutahi</doc_author"> Role, <doc_source id="B75pKCtWyh">BBC</doc_source"> News, <location id="U7BTyqmWFx">Nairobi</location"> <doc_date id="tOpQm0dB9l">15 novembre 2019</doc_date"> Le maïs et ses dérivés sont susceptibles d'être contaminés par une substance appelée <bio_toxin id="cuVejfktbf">aflatoxine</bio_toxin">, celle-ci est toxique et cancérigène, selon l'<organization id="AGyP4CPCSx">OMS</organization">. Plusieurs marques bien connues de farine de maïs ont été retirées des rayons des supermarchés au <location id="qHoI_rYzR6">Kenya</location">, après un avertissement concernant les niveaux de dangerosité de cette substance toxique. Cette situation a suscité de vives inquiétudes, le maïs étant la principale denrée de base du pays. La farine est utilisée pour préparer l'Ugali, une pâte amylacée cuite dont les ingrédients clés sont la farine et l'eau. Le maïs est également utilisé pour préparer un autre plat traditionnel de la région, le Githeri, qui est un mélange de maïs et de haricots, cuits ensemble. Le maïs n'est pas seulement un plat courant dans la plupart des ménages kenyans, c'est aussi un aliment familier dans l'Est, le Centre et le Sud de l'<location id="9l4yW4i91i">Afrique</location">, sous différents noms tels que Nshima, Sima, Sadza, ou Posho. En fait, l'<loc_ref_to_org id="OF1fVbXp3w">Afrique</loc_ref_to_org"> consomme 30% du maïs produit dans le <location id="0VRCSvnaAH">monde</location">, selon les recherches. Une portion d'Ugali, un plat à base de farine de maïs, vue dans un restaurant de <location id="G8VvFyFiVm">Nairobi</location">, au <location id="NiOqkDEsJN">Kenya</location">, le <abs_date id="eTGCGhawUR">24 mai 2017</abs_date">. Mais le maïs n'est pas le seul aliment susceptible d'être contaminé par l'<bio_toxin id="1EmC8HkX_c">aflatoxine</bio_toxin">. En <location id="nOezyniTRC">Afrique de l'Est</location">, le maïs, le lait et les arachides sont les principales denrées d'exposition à cette substances toxiques. Ceux-ci sont généralement mélangés pour faire une bouillie pour les nourrissons et les enfants, ce qui expose ces derniers à un risque particulier d'intoxication par les <bio_toxin id="V2jKbXalIt">aflatoxines</bio_toxin">. Pour le <loc_ref_to_org id="SbB5XEGy9t">Kenya</loc_ref_to_org">, la contamination par les <bio_toxin id="cZv5Mvwp6i">aflatoxines</bio_toxin"> est un problème de longue date. Le pays est considéré comme un point critique mondial, avec des incidents de toxicité aiguë enregistrés en <abs_period id="8EIF-yGhDY">2004</abs_period"> et <abs_period id="zqusfaJ0tn">2010</abs_period">. Il est probable qu'un problème alimentaire dans un pays puisse avoir un effet sur ses voisins, car les produits agricoles font souvent l'objet d'échanges transfrontaliers. Déjà, l'<loc_ref_to_org id="NlNPjX4VcA">Ouganda</loc_ref_to_org"> et le <loc_ref_to_org id="nBr1DAeOy3">Rwanda</loc_ref_to_org"> ont interdit les marques d'arachides importées du <location id="pX41eSxPOG">Kenya</location"> après que le <organization id="6inJoa0bGf">Kenya Bureau of Standards</organization"> (<organization id="zdK9gwJKw7">Kebs</organization">) les a inscrites sur la liste noire en raison de niveaux dangereux d'<bio_toxin id="7rpgkGjsDE">aflatoxines</bio_toxin">. Comment savez-vous quelle farine est sans danger ? <organization id="5SU63jmYXp">Kebs</organization"> qui est chargé d'assurer la qualité globale des normes dans l'industrie, a suspendu les licences de cinq marques de farine de maïs et ordonné leur retrait du marché. Il s'agit du Dola, fabriqué par <organization id="a-i9iLEM4X">Kitui Flour Mills</organization">, du Starehe, fabriqué par <organization id="jGPldQzzPC">Pan African Grain</organization"> et du Kifaru, par <organization id="FfnFY4Jzts">Alpha Grain Limited</organization">. Les autres marques interdites sont 210 (<organization id="7LHkM84zrB">Kenblest Limited</organization">) et Jembe by <organization id="WrL_WX3Ilc">Kensalrise Limited</organization">. Toutes ces marques sont vendues partout au pays. L'agence gouvernementale a déclaré que la suspension faisait suite à une surveillance du marché et à des tests qui ont établi que ces marques avaient des niveaux d'<bio_toxin id="Ex9nj72T5Z">aflatoxines</bio_toxin"> plus qu'acceptables. Mais une association représentant les producteurs de farine de céréale du pays a protesté contre l'interdiction, contestant la validité des méthodes utilisées pour tester les niveaux d'<bio_toxin id="P7gZgsfLhh">aflatoxines</bio_toxin">. Ils disent que d'autres tests indépendants ont donné des résultats différents. En effet, les tests commandés par une station de télévision locale pour un reportage d'investigation ont eu un résultat différent. Le reportage de <organization id="O3WZ4faIQg">NTV</organization"> indiquait que trois marques différentes, Jogoo, Jimbi et Heri, présentaient des niveaux d'<bio_toxin id="WqlaEvZfFO">aflatoxine</bio_toxin"> dangereux - à 13,8, 16,2 et 16,19 parties par milliard (microgramme par kilogramme) respectivement. <organization id="B8U9t0LDJk">Kebs</organization"> considère que des quantités de maïs et d'autres céréales supérieures à 10 par milliard ne sont pas sûres. Cependant, le reportage télévisé indiquait que ses tests sur la marque de farine de maïs Kifaru, que <organization id="IEDUwnTm3-">Kebs</organization"> a suspendue, avaient révélé qu'elle n'était pas affectée par l'<bio_toxin id="YJtDNsfZov">aflatoxine</bio_toxin">. Pour les consommateurs, tout cela est confus et il est difficile de s'assurer que les dizaines de produits à base de maïs qui restent en vente sont sûrs. "Quelqu'un peut-il me donner la raison pour laquelle seules les cinq marques de farine ont été retirées du marché ? Tous les producteurs de farine achètent du maïs au <organization id="tmkCYChLQR">Kenya National Cereals and Produce Board</organization">, une structure qui appartient au <organization id="BHbDYBVPfj">gouvernement</organization">", a déclaré Morphat Gold sur <organization id="GbKDSTAOnq">Twitter</organization">. Une personne du nom de Potentash a twitté : "Effrayant. Nous devons demander des comptes au <organization id="hP15TzVzlk">gouvernement</organization">. Ils ont la responsabilité de s'assurer que les aliments que nous mangeons sont propres à la consommation."

##Résultat##

[{"central": ["YJtDNsfZov", "WqlaEvZfFO", "cuVejfktbf", "1EmC8HkX_c"], "associated": [["tOpQm0dB9l"], ["qHoI_rYzR6", "6E06_QqXdM", "NiOqkDEsJN", "pX41eSxPOG"]]}, {"central": ["qHoI_rYzR6", "6E06_QqXdM", "NiOqkDEsJN", "pX41eSxPOG"], "associated": [["8EIF-yGhDY"], ["V2jKbXalIt", "7rpgkGjsDE", "Ex9nj72T5Z", "cZv5Mvwp6i", "P7gZgsfLhh"]]}, {"central": ["qHoI_rYzR6", "6E06_QqXdM", "NiOqkDEsJN", "pX41eSxPOG"], "associated": [["zqusfaJ0tn"], ["V2jKbXalIt", "7rpgkGjsDE", "Ex9nj72T5Z", "cZv5Mvwp6i", "P7gZgsfLhh"]]}]

#Exemple#

##Texte annoté en entités##

 Sciences & Innovations Environnement <doc_author id="jvkmyyypUf">Aberkane</doc_author"> : ces venins qui valent trente mille fois plus que l'or Les neurotechnologies ont besoin des peptides contenus dans les venins et que nous ne savons pas encore synthétiser. Mais ils ont bien plus à nous apprendre. Par <doc_author id="LuSs4qLw9h">Idriss J. Aberkane</doc_author"> Publié le <doc_date id="uE3rQdx6fM">26/10/2014</doc_date"> à 12h03 La toxine <bio_toxin id="5iEaemOMU8">APETx2</bio_toxin"> d'Anthopleura elegantissima se négocie à 600 euros le milligramme. Si un jour vous entendez un de ces pseudo-docteurs en écologie industrielle ou un de ces Nobel d'économie du café des sports disserter sur l'intérêt de bétonner la barrière de corail ou d'industrialiser la forêt primaire pour mettre au travail ces paresseux de natifs, parlez-lui de la tarentule chinoise ou du cône du <location id="ZVDiDrzSoa">Pacifique</location">. À côté de ce petit mollusque ultra-venimeux, la poule aux oeufs d'or fait figure de plaisanterie. La mu-conotoxine <bio_toxin id="YclLqBpGdz">GIIIB</bio_toxin"> se négocie à presque 500 euros le milligramme chez <organization id="t6E5qqm1QF">Alomone Labs</organization">. La variante <bio_toxin id="XkhzV0H7Np">PIIIA</bio_toxin"> est, elle, à 800 euros le milligramme chez <organization id="p-cFSEDEWj">Smartox Biotech</organization">... 800 millions d'euros le kilo ! Le platine et l'<toxic_c_agent id="ZDeBxzAcDk">héroïne</toxic_c_agent"> pure ? Du terreau de jardin en comparaison. La newsletter sciences et tech Tous les <rel_date id="T2AkjK1rJE">samedis</rel_date"> à 16h Recevez toute l’actualité de la sciences et des techs et plongez dans les Grands entretiens, découvertes majeures, innovations et coulisses... En vous inscrivant, vous acceptez les conditions générales d’utilisations et notre politique de confidentialité. Certaines variantes de la <bio_toxin id="u-lzLmw0VL">jingzhao toxine</bio_toxin">, issues du venin de la tarentule chinoise (<bio_toxin id="OW1vAmJWpF">Chilobrachys jingzhao venom</bio_toxin">), frisent 1 000 euros le milligramme, soit un milliard le kilo. L'<bio_toxin id="Z2GJ6ySp0O">hainantoxine</bio_toxin">, extraite elle de l'araignée chinoise Ornithoctonus hainana, se négocie à 950 euros le milligramme. En comparaison, l'anémone de mer (Anthopleura elegantissima) ferait presque figure de parent pauvre avec sa toxine <bio_toxin id="slQzpv49GG">APETx2</bio_toxin"> à 600 euros le milligramme. Quant au peptide toxique <bio_toxin id="xcj8DCdkIt">Tx2-6</bio_toxin"> de l'araignée très agressive Phoneutria, étudié dans le traitement des troubles érectiles, son coût de synthèse n'est pas encore disponible. Pourquoi une telle inflation ? À l'origine d'une telle envolée des venins, l'essor des neurotechnologies, les nouvelles biotechnologies, qui dopent la demande mondiale en peptides que nous ne savons pas synthétiser facilement, voire pas du tout, et qui doivent alors être collectés sur la bête. Les <bio_toxin id="GO_ukaBDMU">conotoxines</bio_toxin">, <bio_toxin id="23nia60mdT">jingzhaotoxines</bio_toxin">, <bio_toxin id="n6zqySCzz6">huwentoxines</bio_toxin"> et <bio_toxin id="EuqyhY-CbX">hainantoxines</bio_toxin"> affectent différents canaux à sodium, dont ceux que les neuroscientifiques inhibent pour révéler leur potentiel d'action et qui sont aussi nécessaires aux neurones pour communiquer entre eux. On utilise bien évidemment les venins en pharmaceutique, diverses toxines de scorpion traitant les <non_inf_disease id="zCgEGZhxwh">polyarthrites rhumatoïdes</non_inf_disease"> ou les <non_inf_disease id="NWe7GoMMC8">scléroses en plaques</non_inf_disease">. Le venin du cobra royal peut être employé comme analgésique. Quant à l'<bio_toxin id="837Fc1OOA_">épibatidine</bio_toxin">, un alcaloïde accumulé par la grenouille Epipedobates tricolor à partir des insectes dont elle se nourrit, elle est 200 fois plus puissante que la morphine ! Mais la leçon économique des venins ne s'arrête pas à la valeur brute, encore hautement volatile vers le haut (quand l'espèce s'éteint) ou vers le bas (quand on sait facilement reproduire son venin). La nature est une bibliothèque : lisons-la au lieu de la brûler ! C'est la leçon de la biomimétique, la science qui étudie les procédés naturels pour les traduire en savoir-faire humains (réservés aux abonnés). Le principe de la reine rouge Si, par exemple, les cônes produisent une telle diversité de toxines, c'est probablement en raison du "principe de la reine rouge" selon lequel en évolution parfois "il faut courir pour rester à la même place", comme le dit la reine rouge dans Alice au pays des merveilles. Bref, continuer à évoluer et à se diversifier pour survivre, une intéressante leçon industrielle que la sidérurgie allemande a très bien comprise, au grand dam de la nôtre. Meilleure leçon encore : celle du couple proie-prédateur composé de la salamandre Taricha granulosa et du serpent Thamnophis sirtalis en <location id="nQh-SCUwcT">Californie</location">. Dans la compétition entre la salamandre toxique et le serpent résistant, ce dernier a toujours un temps d'avance sur son prédateur. Hanifin et al. (<abs_period id="SuGsepmWrq">2008</abs_period">) [1] ont démontré que là où la salamandre fait de la compétition quantitative (travailler plus pour gagner plus) en produisant plus de sa <bio_toxin id="SuLhdmGTGC">tétrodotoxine</bio_toxin">, le serpent fait de la compétition qualitative en produisant un nouvel antidote : travailler mieux pour gagner... beaucoup plus.

##Résultat##

[]

#Exemple#

##Texte annoté en entités##

 La <loc_ref_to_org id="914WXS0XT8">Polynésie</loc_ref_to_org">, seul pays au monde « à fabriquer de la <bio_toxin id="Rtqy6FFo0T">ciguatoxine</bio_toxin"> pure » <doc_date id="dRm5ATmv6x">16 Avr 2019</doc_date"> Vaite Urarii Pambrun Vaite Urarii Pambrun Lors de l’inauguration de l’exposition célébrant les 70 ans de L’<organization id="iEj_Tk3dhF">Institut Louis Malardé</organization">, le président du Pays a annoncé que la <loc_ref_to_org id="QtfUl1gXGY">Polynésie</loc_ref_to_org"> va se doter d’un « centre de production de micro-algues » à <location id="Tgz0Q7QqvX">Paea</location">. Une algue endémique « recherchée par les laboratoires » pour l’alimentaire et la biomédecine. Selon le docteur Raymond Bagnis, la <loc_ref_to_org id="OMLRSyiHHr">Polynésie</loc_ref_to_org"> est le seul pays au monde « à fabriquer de la <bio_toxin id="ZZ48ni28Je">ciguatoxine</bio_toxin"> pure ».   Les 70 ans de l’<organization id="xFoozulc0L">Institut Louis Malardé</organization"> ont été retracés <rel_date id="PlWb5g5x9G">mardi</rel_date"> matin dans le <org_ref_to_loc id="TavkSxze-h">hall de l’Assemblée de la Polynésie</org_ref_to_loc"> au travers de divers exposés. L’occasion de revenir sur les moments forts de cette institution, mais aussi de rendre hommage à William Robinson, ingénieur naval, qui avait décidé de s’investir au fenua et notamment dans la recherche sur la <inf_disease id="lGvGtuR6ah">filariose</inf_disease">, comme nous le précise le directeur de l’Institut, Hervé Varet. Le taote Raymond Bagnis, qui a mis en place le service dédié à la <non_inf_disease id="yboCRv7L8h">ciguatera</non_inf_disease">, était aussi présent lors de cette inauguration. L’<organization id="J6SJlz3e6V">Institut Louis Malardé</organization"> « marche très bien car il est composé de personnes motivées comme nous l’étions à cette époque-là », dit-il. Il estime d’ailleurs que pour les recherches sur la <non_inf_disease id="LLGy7O0wC1">ciguatera</non_inf_disease"> « nous avons la chance d’avoir un milieu marin extraordinaire, et que l’Institut soit tourné vers la recherche appliquée à la population ». Selon lui la <loc_ref_to_org id="M6BQsw1DQU">Polynésie</loc_ref_to_org"> est le seul Pays au monde « à fabriquer de la <bio_toxin id="gvmxGs3Hl9">ciguatoxine</bio_toxin"> pure ». Le président du Pays a d’ailleurs annoncé dans son discours que de nouvelles infrastructures seront mises à disposition de l’<organization id="Vt4kLmCrBw">Institut Malardé</organization"> à <location id="5SCbXbOWoW">Paea</location">. Il s’agira notamment d’ « un centre de production de microalgues qui permettra de valoriser la chimiodiversité d’une algue endémique (…) recherchée par les laboratoires »  dans les domaines de l’alimentaire et de la biomédecine. Le président du Pays compte bien travailler avec les pays du <location id="WVALI5Gwua">Pacifique</location"> pour « partager les recherches et les connaissances ».

##Résultat##

[{"central": ["Rtqy6FFo0T", "ZZ48ni28Je", "gvmxGs3Hl9"], "associated": [["Tgz0Q7QqvX", "5SCbXbOWoW"], ["PlWb5g5x9G", "dRm5ATmv6x"]]}]

#Exemple#

##Texte annoté en entités##

 <loc_ref_to_org id="0xOKceC8cU">Israël</loc_ref_to_org"> aurait utilisé la bombe anti-bunker BLU-109 contre le chef du <organization id="eQqthC8zZL">Hezbollah</organization"> <doc_source id="yIM62M5XtB">Maroc diplomatique<doc_date id="EspJtkE60e">1 octobre 2024</doc_date"></doc_source">1 octobre 2024 <organization id="cBjV5SwYNq">Hezbollah</organization"> Le <rel_date id="uzr_kVpiJc">27 septembre</rel_date">, une opération militaire d’envergure a été menée par les forces armées israéliennes, aboutissant à l’élimination du chef du <organization id="1HOaABsPaK">Hezbollah</organization">. Une frappe aérienne de précision, visant un bunker profondément enfoui à environ 18 mètres sous terre dans le sud de <location id="IQN0SHPsYc">Beyrouth</location">, a entraîné la mort de plusieurs figures importantes de l’organisation, y compris son chef, Hassan Nasrallah. Les avions chasseurs israéliens F-15I Ra’am, auraient utilisé des bombes anti-bunker d’une technologie avancée : les GBU-31(V)3/B. La clé de cette opération résidait dans l’utilisation par l’<organization id="VpHTUbPMSo">armée de l’air israélienne</organization"> de chasseurs F-15I Ra’am, chacun équipé de six bombes anti-bunker d’une technologie avancée : les GBU-31(V)3/B. Ces bombes, dotées de l’ogive pénétrante BLU-109, sont très puissantes grâce à leur capacité à atteindre des cibles fortifiées bien en dessous de la surface terrestre. Conçue pour des opérations nécessitant la destruction de structures très protégées, l’ogive BLU-109 est le fruit d’une ingénierie de haute précision. Elle pèse environ 874 kg et contient 240 kg de charge explosive. L’élément déterminant de cette ogive réside dans sa coque en acier à haute résistance, spécialement conçue pour maintenir l’intégrité de l’arme lors de l’impact. Cette conception unique permet une pénétration efficace de 1,8 à 2,4 mètres de béton armé avant que la charge explosive ne détonne, une capacité cruciale pour neutraliser des cibles profondément enfouies. Lire aussi : <loc_ref_to_org id="Q2l9mazR49">Israël</loc_ref_to_org"> a lancé une offensive terrestre contre le <organization id="I62ZawbT0h">Hezbollah</organization"> au <location id="aONbLyN6-i">Liban</location"> L’efficacité de la GBU-31(V)3/B est en grande partie due à sa charge composée de <explosive id="vkMGuHc2Wz">tritonal</explosive">. Ce puissant explosif est un mélange de 80 % de <explosive id="2M8HDOzQ-T">TNT</explosive"> et de 20 % de poudre d’aluminium. Ce mélange spécifique a été choisi pour son rendement énergétique élevé. Le <explosive id="f9pfQ3MU5_">tritonal</explosive"> est réputé pour sa capacité à générer une explosion suffisamment puissante pour détruire des infrastructures à la structure complexe et renforcée, comme celles souvent utilisées par des organisations militaires non-étatiques telles que le <organization id="Bu-9r5zywd">Hezbollah</organization">. L’utilisation de telles armes sophistiquées illustre la volonté d’<loc_ref_to_org id="4jPwFhQcno">Israël</loc_ref_to_org"> de cibler avec précision des infrastructures stratégiques qui représentent une menace importante. Cette frappe aérienne, bien que réussie sur le plan opérationnel, soulève toutefois des questions sur les implications géopolitiques et humanitaires de l’utilisation de telles armes dans des zones densément peuplées. En ciblant directement le leadership du <organization id="2guXfZmECP">Hezbollah</organization">, <loc_ref_to_org id="X3MTyURcxB">Israël</loc_ref_to_org"> veut aussi envoyer un message à l’organisation et à ses partisans. La nouvelle escalade intervient dans un contexte de tension préoccupante dans la région, où l’échiquier politique et militaire est marqué par une incertitude quant à l’évolution future des relations entre <loc_ref_to_org id="cP6QlF1Oj1">Israël</loc_ref_to_org"> et ses voisins.

##Résultat##

[{"central": ["vkMGuHc2Wz", "f9pfQ3MU5_"], "associated": [["2M8HDOzQ-T"], ["uzr_kVpiJc"], ["IQN0SHPsYc"]]}]

#Exemple#

##Texte annoté en entités##

 Le <explosive id="u9Bz4SD_r5">TATP</explosive"> : un redoutable explosif facile à fabriquer On l'appelle "la mère de Satan", et de <location id="30OrpBGkS2">Raqqa</location"> à <location id="fnxdv-54ud">Bruxelles</location">, c'est l'explosif préféré des djihadistes de l'organisation <organization id="CSaW1cjYWq">État islamique</organization">. Explications. Source <doc_source id="aqbzDwMZCN">AFP</doc_source"> Publié le <doc_date id="KgRLbfkjkA">23/03/2016</doc_date"> à 17h41 À la suite d'une explosion dans une rame de métro à <location id="pVckzX2zkD">Bruxelles</location">, installation d'un hôpital de campagne <location id="0wTdlkW2lH">rue de la Loi</location">. © Danny GYS/REPORTERS-<organization id="V_P0JTw__o">REA</organization"> C'est une poudre blanche, discrète, facile à fabriquer, mortelle. À <location id="P51Quf6Vo3">Bruxelles</location"> <rel_date id="iJO6QR25Fl">mardi</rel_date">, comme au <org_ref_to_loc id="QFQSYZ5WCA">Bataclan</org_ref_to_loc"> à <location id="3Tnv-_VtwO">Paris</location"> ou sur les champs de bataille syriens, le <explosive id="GKG3EP4Dic">TATP</explosive">, surnommé dans les milieux djihadistes « la mère de Satan », s'avère être un explosif de choix pour le groupe <organization id="RXfUKwIRgX">État islamique</organization">. « Quinze kilos d'explosif de type <explosive id="YfEP5cs7q2">TATP</explosive">, 150 litres d'<toxic_c_agent id="892vVrvgee">acétone</toxic_c_agent">, 30 litres d'<toxic_c_agent id="VoOF99ZDf3">eau oxygénée</toxic_c_agent">, des détonateurs, une valise remplie de clous et de vis » ont été trouvés dans un appartement des kamikazes de <location id="M4dyG8eANH">Bruxelles</location">, a révélé <rel_date id="TMXBpKamy5">mercredi</rel_date"> le procureur fédéral belge Frédéric Van Leeuw. Découvert à la <fuzzy_period id="irBrs9m_Do">fin du XIXe siècle</fuzzy_period"> par un chimiste allemand, le <explosive id="tmxsz6K2RN">peroxyde d'acétone</explosive"> (en anglais <explosive id="89Ya_Ip7El">TATP</explosive"> : <explosive id="V4oejnoyOB">triacetone triperoxide</explosive">) est un explosif artisanal obtenu en mélangeant, dans des proportions précises, de l'<toxic_c_agent id="K-eV3_IpKS">acétone</toxic_c_agent">, de l'<toxic_c_agent id="qN_SrHfTiW">eau oxygénée</toxic_c_agent"> et un <toxic_c_agent id="EJm_lDKX1p-QBvVfQRsMd"><toxic_c_agent id="EJm_lDKX1p-jlrzbl4I8G"><toxic_c_agent id="EJm_lDKX1p-r6hAbDc31Q">acide (sulfurique</toxic_c_agent">, chlorhydrique</toxic_c_agent"> ou nitrique</toxic_c_agent">), produits faciles à trouver dans le commerce. On obtient alors une poudre constituée de cristaux blancs, ressemblant à un sucre grossier, qu'un détonateur simple suffit à faire exploser, dans une déflagration produisant un terrible dégagement de gaz brûlants. « Regarder un tutoriel ne suffit pas » Ces dernières années, en <location id="hn7DoES97o">Irak</location"> et en <location id="QVxJe7fHb6">Syrie</location">, les laboratoires, d'abord sommaires puis quasi industriels, de <explosive id="-1Lg1gLfds">TATP</explosive"> et d'autres matières explosives artisanales se sont multipliés. Dans un rapport publié en <rel_period id="N2NvL-7h_9">février</rel_period">, l'ONG <organization id="aIC1s2VAzq">Conflict Armament Research</organization"> a mis au jour, après une enquête de vingt mois, un réseau de 51 sociétés, basées dans vingt pays, dont la <location id="SNolPWPPaL">Turquie</location">, la <location id="VefhnOXd9H">Russie</location"> mais aussi la <location id="qzbLwJkoG9">Belgique</location"> et les <location id="vAvAfDt7QF">États-Unis</location">, ayant fourni à l'<organization id="5NdmoETNuM">EI</organization"> les composants nécessaires à la fabrication semi-industrielle d'explosifs artisanaux. « Contrairement à ce qu'on dit parfois, regarder un tutoriel sur Internet ne suffit pas », assure à l'<organization id="egUJ8y3hOI">Agence France-Presse</organization"> Éric, un ancien officier du <organization id="fUsXtxHKS5">génie</organization">, spécialiste des explosifs, qui demande à ne pas être davantage identifié. « Il faut quand même que quelqu'un vous ait montré une fois. Mais des instructeurs, les gars de l'<organization id="kyhQ451G_h">État islamique</organization"> n'en manquent pas, en <location id="aDvpLwgOaZ">Syrie</location"> et en <location id="-yCXeofNub">Irak</location">. Puis ça se diffuse de cours pratique en cours pratique. Quand on vous a montré, vous pouvez effectivement le faire dans votre cuisine. » « Ça a pété fort » La partie la plus délicate est l'ajout d'acide au mélange d'<toxic_c_agent id="7BctVCJ-2q">acétone</toxic_c_agent"> et d'<toxic_c_agent id="lW5Qg7Y1Uc">eau oxygénée</toxic_c_agent">, qui dégage de la chaleur, de fortes émanations et peut s'enflammer, mais un opérateur soigneux, protégé par un simple masque, peut y parvenir sans peine. C'est de <explosive id="ver5b8h5VO">TATP</explosive"> qu'étaient constituées les ceintures explosives des kamikazes du <rel_date id="8QdtgtKOg6">13 novembre</rel_date"> à <location id="QqwLgfR3pR">Paris</location">, comme, selon les premières présomptions, les gilets et bombes que les djihadistes ont fait sauter <rel_date id="qlQygmBwX3">mardi</rel_date"> dans l'aéroport et le métro de <location id="IHyZ3M5rYC">Bruxelles</location">, faisant au moins 31 morts et 270 blessés, dont beaucoup souffrent de graves brûlures. Pour provoquer l'explosion du <explosive id="v2hEdT-dak">TATP</explosive">, un détonateur est nécessaire. Il peut être fabriqué, à l'aide d'un fin tube métallique rempli de pâte et relié à deux fils électriques qui, mis en contact, vont provoquer un arc électrique puis une flamme. Plus simplement, ils peuvent être achetés dans le commerce. C'est ce qu'a fait Salah Abdeslam, l'un des djihadistes du <rel_date id="cw2JD8-qdM">13 novembre</rel_date">, arrêté le <rel_date id="jLw7tebTmD">18 mars</rel_date"> à <location id="AEF1Rc9mod">Bruxelles</location"> : après avoir laissé photocopier son permis de conduire, il avait acheté une dizaine de détonateurs pyrotechniques chez un vendeur de matériel pour feux d'artifice de la <location id="EHLjCkmoz2">région parisienne</location">, sans éveiller le moindre soupçon. « Le principal problème que nous pose le <explosive id="xTaAj0agP_">TATP</explosive"> », confie à l'<organization id="PyGRQNAJAT">Agence France-Presse</organization"> un membre des services français antiterroristes, qui demande à rester anonyme, « c'est la disponibilité des ingrédients. On peut surveiller les ventes d'<toxic_c_agent id="9P5fdo_8I2">eau oxygénée</toxic_c_agent">, d'ailleurs on le fait bien sûr, mais si les gars sont assez malins pour faire vingt pharmacies et acheter de petites quantités, ça passe. Pareil pour l'<toxic_c_agent id="JJ0zheDvb-">acétone</toxic_c_agent"> et l'acide... » « Lors d'un stage, on a passé l'après-midi à fabriquer des explosifs artisanaux, notamment du <explosive id="kvtB9mlp0o">TATP</explosive">, ensuite testés. C'est d'une facilité déconcertante. Uniquement avec des produits achetés » dans des magasins de bricolage. « En une demi-heure, on avait fabriqué l'explosif, une demi-heure après on le faisait péter. Et ça a pété fort », dit-il.

##Résultat##

[{"central": ["fnxdv-54ud", "IHyZ3M5rYC", "pVckzX2zkD", "AEF1Rc9mod", "P51Quf6Vo3", "M4dyG8eANH"], "associated": [["iJO6QR25Fl", "qlQygmBwX3"], ["892vVrvgee", "K-eV3_IpKS", "JJ0zheDvb-", "7BctVCJ-2q"], ["qN_SrHfTiW", "9P5fdo_8I2", "lW5Qg7Y1Uc", "VoOF99ZDf3"], ["u9Bz4SD_r5", "GKG3EP4Dic", "xTaAj0agP_", "kvtB9mlp0o", "YfEP5cs7q2", "ver5b8h5VO", "89Ya_Ip7El", "-1Lg1gLfds", "v2hEdT-dak", "tmxsz6K2RN", "V4oejnoyOB"], ["EJm_lDKX1p-r6hAbDc31Q"], ["EJm_lDKX1p-jlrzbl4I8G"], ["EJm_lDKX1p-QBvVfQRsMd"]]}, {"central": ["cw2JD8-qdM", "8QdtgtKOg6"], "associated": [["QqwLgfR3pR", "3Tnv-_VtwO"], ["u9Bz4SD_r5", "GKG3EP4Dic", "xTaAj0agP_", "kvtB9mlp0o", "YfEP5cs7q2", "ver5b8h5VO", "89Ya_Ip7El", "-1Lg1gLfds", "v2hEdT-dak", "tmxsz6K2RN", "V4oejnoyOB"]]}]

#Exemple#

##Texte annoté en entités##

 Sept tonnes d'explosifs en provenance d'<location id="NDeeOG9ESL">Iran</location"> saisies dans un port italien Les autorités italiennes ont saisi sept tonnes de <explosive id="RJP37xet25">RDX</explosive">, un puissant explosif, expédiées d'<location id="olYxWS3ovA">Iran</location"> en <location id="159z7HVCKy">Syrie</location">, a annoncé <rel_date id="GEpESOCwBv">mercredi</rel_date"> la <organization id="QMZDpo71FJ">police</organization">. Publié le : <doc_date id="plpRI6WaE0">22/09/2010</doc_date"> - 20:48 Modifié le : <doc_date id="HSwPUwTjl2">23/09/2010</doc_date"> - 15:07 Les pains explosifs ont été découverts la <rel_period id="7m-ICJTowD">semaine dernière</rel_period"> dans un port de <location id="VhexHNGsgN">Calabre</location"> dans le sud de l'<location id="v3Vy-riuPG">Italie</location">. Ils étaient cachés dans un conteneur plein de lait en poudre. Le conteneur avait été déchargé par un cargo en provenance d'<location id="xjGadpRHyS">Iran</location"> sa destination finale était la <location id="vZlE1E1myt">Syrie</location">. L'annonce de cette prise spectaculaire a été retardée pour faciliter le travail des enquêteurs. Le chef de la <organization id="PCDpdqvHHS">police locale</organization"> a affirmé que la cargaison était arrivée en <location id="aPk6kpyuBp">Italie</location"> grâce à des organisations criminelles. Il n'a pas précisé lesquelles mais la <organization id="lkj0teBqrY">'Ndrangheta</organization">, la <organization id="fuo1Zcibvr">mafia calabraise</organization">, semble être hors jeu. La piste privilégiée est celle d'un trafic international d'explosif. La quantité d'explosif a d'ailleurs impressionné la <organization id="o3-MRP-Akq">police italienne</organization">. Les sept tonnes de <explosive id="Cl0Q_K9BIH">RDX</explosive">, aurait pu faire sauter tout le port à conteneur. Le <explosive id="aRREHt9RRA">RDX</explosive"> est un explosif plastique souple et malléable. Sa stabilité en fait un des explosifs les plus couramment utilisés par les militaires depuis la Seconde Guerre mondiale et par les ingénieurs dans le secteur de la construction. Il est également très prisé par les terroristes et par la mafia.

##Résultat##

[{"central": ["Cl0Q_K9BIH", "aRREHt9RRA", "RJP37xet25"], "associated": [["olYxWS3ovA", "NDeeOG9ESL", "xjGadpRHyS"], ["7m-ICJTowD"], ["VhexHNGsgN"]]}]

#Exemple#

##Texte annoté en entités##

 Recrudescence des cas de <inf_disease id="DFUIOXQc2I">leptospirose</inf_disease">, en <fuzzy_period id="2x0v14G8gM">ce début d'année</fuzzy_period">  Soixante-trois cas de <inf_disease id="OKxGIt3P6t">leptospirose </inf_disease">ont déjà été recensés, <rel_period id="KuA-7YqWDH">depuis le mois de janvier</rel_period">, en <location id="FBrw8rB6PX">Nouvelle-Calédonie</location">. Cinquante-cinq patients ont dû être hospitalisés, dont 20 en réanimation. La maladie du rat sévit, chaque année, <fuzzy_period id="UURXPnQZQW">durant la saison des pluies</fuzzy_period">. <doc_author id="siugN6pJK7">Martine Nollet</doc_author"> (<doc_author id="fRD2lqxobG">Gédéon Richard</doc_author">)  Publié le <doc_date id="FZtxiRV60R">2 mars 2022</doc_date"> à 11h15, mis à jour le <doc_date id="EXycCYbiPi">2 mars 2022</doc_date"> à 11h54  En cas de fatigue, de fièvre élevée, de douleurs musculaires, articulaires et abdominales, consultez un médecin au plus vite. L’<rel_period id="DonyrPoJ6h">an dernier</rel_period">, quatre personnes sont décédées de la <inf_disease id="TVB6CbgjKo">leptospirose</inf_disease">. <fuzzy_period id="hIdsHJzM-y">Depuis le début de l'année</fuzzy_period">, 63 cas de contamination à cette bactérie, appelée maladie du rat, ont été recensés, dont 87% ont conduit à une hospitalisation.  La <location id="xk13VZhobp">Nouvelle-Calédonie</location"> n'est pas épargnée par cette maladie grave, parfois mortelle. L'<rel_period id="pt0kkema-o">an dernier</rel_period">, 229 cas ont été déplorés. "C'est une maladie que l'on retrouve plus fréquemment en <fuzzy_period id="eBXZ6JXuy2">début d'année</fuzzy_period">. Il faut diagnostiquer suffisamment tôt cette pathologie, pour qu'elle soit traitée le plus rapidement possible", explique Stéphane Chabaud, infirmier référent <inf_disease id="YzQXof4vCD">leptospirose</inf_disease">. Une maladie davantage présente en <location id="ZkD4td-SZW">province Nord</location">  "Le moment entre lequel nous sommes affectés et celui où nous déclarons des signes cliniques varie, à peu près, d'une à trois semaines. En début de maladie, les signes peuvent ressembler à d'autres maladies, comme la <inf_disease id="rVdk8lBYX2">dengue </inf_disease">et la <inf_disease id="QWlcDgGYpU">Covid-19</inf_disease">. Si on attend, [on observe, NDLR] une apparition de jaunisse", complète le docteur Anne Pfannstiel, médecin de prévention à la <organization id="4K3mDYUEcj">Dass-NC</organization"> (<organization id="hXcDGtzaMZ">Direction de l'agence sanitaire et sociale</organization">).  "Nous avons une recrudescence de cas, habituellement, dans le <rel_period id="hJesx8UWJB">premier semestre de l'année</rel_period">. En <abs_period id="EaLvS76w08">1999</abs_period">, nous avions eu 19 décès dus à la <inf_disease id="OkL2DLYiHH">leptospirose</inf_disease">", poursuit-elle. En deux mois, en <abs_period id="ziPSWkxfgz">2022</abs_period">, 63 cas ont été comptabilisés. "C'est énorme, avec 22 enfants touchés. Les deux tiers des cas concernent la <location id="P8XPnXvjCq">province Nord</location"> ", précise le docteur. La <location id="XzNejyvmJH">province des Iles Loyauté</location"> est, a contrario, épargnée. <rel_period id="Mvxco1444j">Depuis le mois de janvier</rel_period">, le patient le plus jeune est âgé de 6 ans. Le plus âgé a 71 ans. La plus grande prudence est donc recommandée, d'autant que cette maladie peut être évitée.  Eviter de marcher pieds nus  "La peau est une très très bonne barrière. C'est pour cela que nous recommandons fortement aux personnes d'éviter de marcher pieds nus. Si nous limitons ce risque, en portant des chaussures et en portant des gants, cela constitue une barrière. En cette période très pluvieuse, il y a un risque de contracter cette bactérie", insiste Stéphane Chabaud. Autrement dit, évitez de marcher pieds nus, surtout si vous avez des plaies.  La <inf_disease id="37QD-xjlSs">leptospirose </inf_disease">est causée par des bactéries qui se trouvent dans les urines des rongeurs et d'autres mammifères. Elle peut s’attraper plusieurs fois et se contracte en cas de contact avec les eaux, les sols, par la peau et surtout par les muqueuses. Cette bactérie peur survivre plusieurs mois dans un milieu humide.

##Résultat##

[{"central": ["OkL2DLYiHH", "OKxGIt3P6t", "37QD-xjlSs", "DFUIOXQc2I", "TVB6CbgjKo", "YzQXof4vCD"], "associated": [["Mvxco1444j", "KuA-7YqWDH"], ["FBrw8rB6PX", "xk13VZhobp"], ["ZkD4td-SZW", "P8XPnXvjCq"]]}, {"central": ["OkL2DLYiHH", "OKxGIt3P6t", "37QD-xjlSs", "DFUIOXQc2I", "TVB6CbgjKo", "YzQXof4vCD"], "associated": [["FBrw8rB6PX", "xk13VZhobp"], ["DonyrPoJ6h", "pt0kkema-o"]]}, {"central": ["OkL2DLYiHH", "OKxGIt3P6t", "37QD-xjlSs", "DFUIOXQc2I", "TVB6CbgjKo", "YzQXof4vCD"], "associated": [["FBrw8rB6PX", "xk13VZhobp"], ["EaLvS76w08"]]}, {"central": ["OkL2DLYiHH", "OKxGIt3P6t", "37QD-xjlSs", "DFUIOXQc2I", "TVB6CbgjKo", "YzQXof4vCD"], "associated": [["Mvxco1444j", "KuA-7YqWDH"], ["XzNejyvmJH"]]}]

#Exemple#

##Texte annoté en entités##

 <location id="haBY6AR3Ug">Irak</location">: 27 décès dus à la<inf_disease id="6nAPGGyp7g"> fièvre du Congo</inf_disease"> <fuzzy_period id="X5tDhtGkqP">depuis le début de l'année</fuzzy_period"> <doc_date id="O13RL8wqnG">11 juin 2022</doc_date"> Par WWW.DEFIMEDIA.INFO Contact: webmaster@defimedia.info Des hommes désinfectant une ferme du <location id="jLMdXBl-YR">village d'al-Bojari</location">, dans la <location id="FMPxWTdRfl">province de Dhi Qar</location">, dans le sud de l'<location id="99kGsR3bPa">Irak</location">, en <abs_period id="sX-2RwqPwo">mai 2022</abs_period">. Photo : <organization id="sJEFZs23Sb">L’orient- Le jour</organization">/ <organization id="POKYdXkb4J">AFP</organization">/ ASSAAD NIAZI  Au moins 27 personnes sont mortes en <location id="BHQ-H9c1ad">Irak </location">de la <inf_disease id="4R6_jz3Uhy">fièvre du Congo</inf_disease"> <fuzzy_period id="8OKk6gdz3P">depuis le début de l'année</fuzzy_period">, un bilan en hausse diffusé <rel_date id="vvffIKTSlA">samedi </rel_date">par les autorités qui tentent de freiner la propagation de cette maladie transmise par le bétail.  Un précédent bilan officiel avait fait état<rel_date id="6aXfU1hxTL"> il y a un mois</rel_date"> de 12 décès dus à cette <inf_disease id="gs0cWi6_dk">fièvre hémorragique</inf_disease"> <fuzzy_period id="yfU6gbwPhh">depuis début 2022</fuzzy_period">.  La transmission de la maladie se produit "soit par les piqûres de tiques, soit par contact avec du sang ou des tissus d'animaux infectés, pendant ou immédiatement après l'abattage", selon l'<organization id="xwh2h_2ECr">Organisation mondiale de la santé</organization"> (<organization id="dZb9QwYIWx">OMS</organization">).  "<fuzzy_period id="HtL78b1El_">Depuis le début de l'année</fuzzy_period">, 162 cas de <inf_disease id="emfCAECbhY">fièvre hémorragique</inf_disease"> ont été recensés, dont 27 décès. La moitié des personnes affectées sont désormais rétablies", a déclaré le porte-parole du <organization id="hme5LPQN41">ministère de la Santé</organization">, Seif al-Badr, relevant qu'un premier décès avait été enregistré dans la <location id="l13st2ITDs">région automne du Kurdistan</location">, dans le nord de l'<location id="-w4vc8pa9J">Irak</location">.  Le <organization id="9m9oN-o0YK">ministère de la Santé</organization"> s'efforce de "détecter les cas de la façon la plus précoce possible", a assuré M. Badr.  De nombreux cas (61) ont été recensés à<location id="t5i4KaS881"> Dhi Qar</location">, une province pauvre et rurale du sud du pays où sont élevés des bovins, des moutons et des chèvres, animaux qui sont autant d'hôtes intermédiaires de la <inf_disease id="Ybzzd4jfU8">fièvre hémorragique de Crimée-Congo</inf_disease"> (<inf_disease id="uQIYrY3o25">FHCC</inf_disease">).  Les autorités font la chasse aux abattoirs qui ne respectent pas les protocoles d'hygiène. Plusieurs provinces ont interdit toute entrée et sortie de bétail de la région et ont lancé des campagnes de désinfection parmi les bêtes.  Selon le <organization id="kdyqmlcKHJ">ministère de la Santé irakien</organization">, les personnes les plus touchées par la <inf_disease id="esAXx58Eg0">fièvre hémorragique</inf_disease"> sont les éleveurs de bétail ainsi que les employés des abattoirs.  Le virus provoque la mort dans 10 à 40% des cas. Entre humains, la transmission de la maladie "peut survenir à la suite d'un contact direct avec du sang, des sécrétions, des organes ou des liquides biologiques de sujets infectés", selon l'<organization id="38ZnmTTpyc">OMS</organization">.  © <organization id="YXaWL5gsei">Agence France-Presse</organization">

##Résultat##

[{"central": ["gs0cWi6_dk", "4R6_jz3Uhy", "6nAPGGyp7g", "uQIYrY3o25", "Ybzzd4jfU8"], "associated": [["99kGsR3bPa", "-w4vc8pa9J", "haBY6AR3Ug", "BHQ-H9c1ad"], ["yfU6gbwPhh", "X5tDhtGkqP", "HtL78b1El_", "8OKk6gdz3P"], ["l13st2ITDs"], ["t5i4KaS881", "FMPxWTdRfl"]]}]

#Exemple#

##Texte annoté en entités##

 La <loc_ref_to_org id="KmTOWt7txE">Guinée </loc_ref_to_org">annonce un cas de <inf_disease id="uact9wEGJF">fièvre de Lassa</inf_disease"> dans le Sud Le virus tire son nom de la <location id="nC4KJV7wrM">ville de Lassa</location"> dans le nord du pays, où il a été pour la première fois identifié en <abs_period id="B5aRqIB3vi">1969</abs_period">. © Crédit photo : <organization id="Pjpe7-GnD4">AFP</organization">/SEYLLOU Par SudOuest.fr avec<organization id="bdBCWT7FRc"> AFP</organization"> Publié le <doc_date id="DoOQQHxsG_">23/04/2022</doc_date"> à 14h40.  Le <pathogen id="irOvTra3V0">virus de la fièvre de Lassa</pathogen"> a été détecté sur une patiente de 17 ans  Les autorités sanitaires de <location id="ELNLOfPwvL">Guinée </location">ont annoncé avoir identifié un cas de <inf_disease id="jXttqJM0ch">fièvre hémorragique de Lassa</inf_disease">, une maladie virale apparentée à <inf_disease id="mYIyFcnK2V">Ebola</inf_disease">, dans le sud du pays, dans un communiqué. Le <pathogen id="6zd-O6OQu5">virus de la fièvre de Lassa</pathogen"> a été détecté sur une patiente de 17 ans « en provenance de la <location id="SmJ-BXNQmX">sous-préfecture de Kassadou</location"> », dans la <location id="aFsgL4ZHRv">préfecture de Guéckédou</location"> (sud), où l’épidémie a été déclarée, a indiqué le <organization id="baQtN9I9p_">ministère de la Santé</organization"> dans un communiqué publié <rel_date id="0efMfrCQaC">vendredi </rel_date">soir.  La pandémie de<inf_disease id="pQDZeSUWy6"> Covid-19</inf_disease"> a causé des « perturbations » selon l’<organization id="WUB4OvE18J">OMS</organization"> dans l’accès au soin et la prise en charge du <inf_disease id="28fSnMFlZ6">paludisme </inf_disease">dans les populations les plus concernées en <location id="EVZzv7R-N4">Afrique</location">  La malade est traitée dans un centre de prise de charge de <location id="jPkRbMJBjs">Guéckédou</location">, dans la <location id="9ops7FGqRo">région de Nzérékoré</location">, et « son état est à ce jour satisfaisant », selon ce communiqué. Le virus a été identifié le <rel_date id="eiZdZc5mR8">20 avril</rel_date"> par un laboratoire de <location id="LWjuQ2YueN">Guéckédou </location">et « un second test réalisé au <location id="c_Vmpzx6qO">laboratoire de référence de Conakry</location"> a confirmé le premier résultat », précise le texte.  Une fièvre sévère  La transmission de la <inf_disease id="w-afNUiam5">fièvre de Lassa</inf_disease"> se fait par les excrétions de rongeurs ou par contact direct avec du sang, des urines, des selles ou d’autres liquides biologiques d’une personne malade. Une fois déclarée, cette fièvre peut causer des hémorragies dans les cas les plus sévères (environ un cas sur cinq)

##Résultat##

[{"central": ["w-afNUiam5", "jXttqJM0ch", "uact9wEGJF"], "associated": [["6zd-O6OQu5", "irOvTra3V0"], ["SmJ-BXNQmX"], ["jPkRbMJBjs", "LWjuQ2YueN"], ["eiZdZc5mR8"]]}, {"central": ["w-afNUiam5", "jXttqJM0ch", "uact9wEGJF"], "associated": [["nC4KJV7wrM"], ["B5aRqIB3vi"], ["6zd-O6OQu5", "irOvTra3V0"]]}]

#Exemple#

##Texte annoté en entités##

 <location id="bdIomqEuHZ">Hong Kong</location">. Des dizaines de personnes atteintes par une <inf_disease id="JL2uHhItGG">hépatite </inf_disease">transmise par les rats  Un nouveau virus est apparu <fuzzy_period id="4DY9NzkXcw">depuis quelques mois</fuzzy_period"> dans la <location id="6LMOWO805J">province chinoise de Hong Kong</location">. Une forme d’<inf_disease id="TxCK8tE4pl">hépatite</inf_disease">, transmise par les rats, a déjà entraîné l’hospitalisation de dizaines de patients. A <location id="istc-J-ap-">Hong Kong</location">, le rat transmet une nouvelle forme d'<inf_disease id="8toJgP_0JN">hépatite </inf_disease">aux humains. | THIERRY CREUX / <organization id="Bamx6hqFv6">OUEST FRANCE</organization">  <doc_source id="v4B8wp1n0A">Ouest France</doc_source"> Publié le <doc_date id="7woUMpEFTp">09/05/2020</doc_date"> à 05h36   Une dizaine d’habitants de <location id="uK-QtA0a2r">Hong Kong</location"> ont été testés positifs à l’<inf_disease id="vF2J-gKos8">hépatite E</inf_disease"> provenant des rats, une maladie également connue sous le nom de <path_ref_to_dis id="Md2VWekAQN">VHE du rat</path_ref_to_dis">. Le cas le plus récent a été découvert le <rel_date id="7_17sgl1p6">30 avril</rel_date"> : un homme de 61 ans présentant une fonction hépatique anormale. Ce patient testé positif pourrait le premier d’une longue liste. Les médecins de <location id="12OS-w9-ap">Hong Kong</location"> estiment en effet qu’il pourrait exister des centaines d’autres personnes infectées par ce virus et non diagnostiquées.  Le premier cas connu est apparu en <abs_period id="S8qZaa8YNP">2018</abs_period">. Cette année-là, des experts en maladies infectieuses de l’<organization id="7NAOBKcijD">Université de Hong Kong</organization"> avaient accueilli un patient inhabituel. Cet homme de 56 ans avait subi une greffe de foie récente, et présentait des fonctions hépatiques anormales sans cause évidente.  Les tests pratiqués sur le patient avaient alors révélé que son système immunitaire réagissait à l’<dis_ref_to_path id="VysVuQL8KM">hépatite E</dis_ref_to_path">, mais sans identifier la souche humaine du <pathogen id="ILnj8L9NSu">virus de l’hépatite E</pathogen"> (<pathogen id="IPQRsl51iU">VHE</pathogen">) dans son système sanguin. L’<inf_disease id="K1BmPI7HRD">hépatite E</inf_disease"> est en effet une maladie du foie provoquant de la fièvre, une jaunisse et une hypertrophie de l’organe.  Le virus se présente en quatre espèces, qui circulent chez différents animaux ; à l’époque, un seul de ces quatre était connu pour infecter les humains.  Virus inquiétant  Équipés de tests spécialement conçus pour cette souche humaine de <pathogen id="YfH4CTH5UX">VHE </pathogen">négatif, les chercheurs ont amélioré le test de diagnostic, l’ont exécuté à nouveau et ont découvert, pour la première fois dans l’histoire, l’<inf_disease id="iQ9MWEg-0_">hépatite E</inf_disease"> du rat chez un humain.  « Ce qui est inquiétant, c’est que ce virus peut passer de l’animal à l’homme », confie le Dr Siddharth Sridhar, microbiologiste et l’un des chercheurs à l’origine de la découverte. « Cette infection était si inhabituelle et sans précédent que l’équipe s’est demandée s’il s’agissait d’un incident ponctuel, ou d’un patient qui était au mauvais endroit au mauvais moment ».  Mais depuis, les cas se multiplient et les médecins craignent que ce virus n’existe en fait depuis plusieurs années et n’ait été « dormant », avant de se transmettre à grande échelle.  Un rapport a donc été réalisé et transmis à l’<organization id="E5mUu8itXq">OMS</organization"> afin d’alerter tous les pays et les aider à se préparer au cas où cette <inf_disease id="aQko-bjiyt">hépatite </inf_disease">deviendrait la prochaine maladie de grande ampleur à toucher la population mondiale.

##Résultat##

[{"central": ["iQ9MWEg-0_", "aQko-bjiyt", "TxCK8tE4pl", "JL2uHhItGG", "vF2J-gKos8", "8toJgP_0JN"], "associated": [["6LMOWO805J", "uK-QtA0a2r", "istc-J-ap-", "12OS-w9-ap", "bdIomqEuHZ"], ["7_17sgl1p6"]]}, {"central": ["6LMOWO805J", "uK-QtA0a2r", "istc-J-ap-", "12OS-w9-ap", "bdIomqEuHZ"], "associated": [["iQ9MWEg-0_", "aQko-bjiyt", "TxCK8tE4pl", "JL2uHhItGG", "vF2J-gKos8", "8toJgP_0JN"], ["S8qZaa8YNP"]]}]

Ci-dessous le texte à traiter
{% set ns = namespace(altsum='') -%}
{% for alt in doc.altTexts -%}
{% if alt.name == 'Annotations' -%}
{% set ns.altsum = alt.text -%}
{% endif -%}
{% endfor -%}
{{ ns.altsum }}
    """
    docs = [Document(**jdoc) for jdoc in jdocs]
    # parameters = DeepInfraOpenAICompletionParameters(
    #     model='meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8',
    #     max_tokens=16000,
    #     temperature=0.2,
    #     prompt=event_prompt,
    #     completion_altText="Event - Llama4-Maverick + Expls"
    # )
    parameters = OpenAICompletionParameters(
        model='gpt-4.1',
        max_tokens=16000,
        temperature=0.2,
        prompt=event_prompt,
        completion_altText="Event - GPT-4.1 + Expls"
    )
    processor = OpenAICompletionProcessor()
    results = processor.process(deepcopy(docs), parameters)
    result_file = Path(testdir, "data/evalllm_2025_new_gpt_4_5_1-documents.json")
    dl = DocumentList(__root__=results)
    with result_file.open("w") as fout:
        fout.write(dl.json(exclude_none=True, exclude_unset=True, indent=2))
