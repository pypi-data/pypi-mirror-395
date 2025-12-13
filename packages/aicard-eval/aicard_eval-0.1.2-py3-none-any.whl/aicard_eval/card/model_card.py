import json
import html2text
import markdown2
import rich
import io

from typing import Union
from rich.markdown import Markdown
from pydantic import BaseModel, create_model
from pydantic import Field as pydantic_Field
from .dot_dict import DotDict
from .fields import ShortText, LongText, Options, Field, Pattern

def truncate(text, size):
    text = text.strip().split(" ")[0].split("\n")[0].split("/")[-1].strip()
    if size<3:
        return ""
    text = str(text)
    size = int(size)
    if len(text)<=size:
        return text
    return text[:(size-3)]+"..."

class ModelCard:
    def __init__(self, connector=None):
        object.__setattr__(self, "data", DotDict(
            title=ShortText(),
            model=DotDict(
                name=ShortText("What is the name of the model?"),
                overview=LongText("An overview of the model. The reader should have a good idea of what the model is, the purpose, novelty, capabilities, and caveats after reading this."),
                author=LongText("What person or organization developed the model?"),
                date=ShortText("When was the model developed?"),
                version=ShortText("Which version of the model is it? e.g. v1.0"),
                type=Options(["unknown", "Linear Regression", "Logistic Regression", "Decision Tree", "Random Forest", "Gradient Boosting", "Naive Bayes", "K-Nearest Neighbors", "Support Vector Machine", "Convolutional Neural Network", "Recurrent Neural Network", "Transformer", "Autoencoder", "Generative Adversarial Network", "Graph Neural Network", "Multilayer Perceptron", "Reinforcement Learning Agent", "Clustering Model", "Dimensionality Reduction Model", "Ensemble Model", "Other"],"What type of model is it? This includes basic model architecture details, such as whether it is a Naive Bayes classifier, a Convolutional Neural Network, etc. This is likely to be particularly relevant for software and model developers, as well as individuals knowledgeable about machine learning, to highlight what kinds of assumptions are encoded in the system."),
                license=LongText("Under which licence is the model published? If necessary, add any other information related to intellectual property (IP)."),
                home=LongText("Where can resources for more information be found?"),
                contact=LongText("E.g., what is an email address that people may write to for further information?"),
                citation=LongText("How should the model be cited? This may include @article or @inproceedings bibtex formats."),
                more=LongText("Additional model information not found above.")),
            considerations=DotDict(
                use_case=LongText("This section details whether the model was developed with general or specific tasks in mind (e.g., plant recognition worldwide or in the Pacific Northwest). The use cases may be as broadly or narrowly defined as the developers intend. For example, if the model was built simply to label images, then this task should be indicated as the primary intended use case."),
                oversight=Options(["unknown","self-learning/autonomous", "human-in-the-loop", "human-on-the-loop", "human-in-command"]),
                users=LongText("For example, was the model developed for hobbyists, or enterprise solutions? This helps users gain insight into how robust the model may be to different kinds of inputs."),
                out_of_scope_use=LongText("Here, the model card should highlight technology that the model might easily be confused with, or related contexts that users could try to apply the model to. This section may provide an opportunity to recommend a related or similar model that was designed to better meet that particular need, where possible. This section is inspired by warning labels on food and toys, and similar disclaimers presented in electronic datasheets. Examples include “not for use on text examples shorter than 100 tokens” or “for use on black-and-white images only; please consider our research group’s full-colour-image classifier for colour images.” Examples include “not for use on text examples shorter than 100 words."),
                software=LongText("What are software requirements and dependencies? If possible, please add a link to an open source repository like GitHub with details on dependencies, the environment and documentation."),
                instructions=LongText("Provide any other information which helps users use the model. Ideally, add a code snippet illustrating a typical use-case. You can also add a link to a GitHub repository with usage instructions. This is inspired by model cards such as this: https://huggingface.co/microsoft/beit-base-patch16-224-pt22k-ft22k"),
                inputs_outputs=LongText("Provide a short description of the model's inputs and outputs"),
                factors=LongText("What are foreseeable salient factors for which model performance may vary, and how were these determined? "),
                hardware=LongText("What are hardware requirements for training and inference (e.g. CPU or GPU)? What do users need to take into account regarding hardware regarding deployment?"),
                more=LongText("Additional considerations not found above.")),
            training_set=DotDict(
                datasets=LongText("What dataset(s) were used tot train the model? If possible, please add a link to details on the respective datasets used, for example a datasheet."),
                motivation=LongText("Why were these datasets chosen?"),
                preprocessing=LongText("How was the data pre-processed for evaluation (e.g., tokenization of sentences, cropping of images, any filtering such as dropping images without faces)? Please provide a short description. You can also add a GitHub link to the respective pre-processing scripts. "),
                standards=Options(["unknown", "none", "ISO","IEEE"]),
                update=Options(["unknown", "no", "yes"], "Did you put in place measures to ensure that the data (including training data) used to develop the AI system is up-to-date, of high quality, complete and representative of the environment the system will be deployed in?"),
                more=LongText("Additional training set information not found above.")),
            eval_set=DotDict(
                datasets=LongText("What dataset(s) were used to evaluate the model? If possible, please add a link to details on the respective datasets used, for example a datasheet."),
                motivation=LongText("Why were these datasets chosen?"),
                preprocessing=LongText("How was the data pre-processed for evaluation (e.g., tokenization of sentences, cropping of images, any filtering such as dropping images without faces)? Please provide a short description. You can also add a GitHub link to the respective pre-processing scripts. "),
                standards=Options(["unknown", "none", "ISO","IEEE"]),
                update=Options(["unknown", "no", "yes"], "Did you put in place measures to ensure that the data (including training data) used to develop the AI system is up-to-date, of high quality, complete and representative of the environment the system will be deployed in?"),
                more=LongText("Additional test set information not found above.")
            ),
            performance=DotDict(
                analysis=LongText("Analyse and explain performance results of your model."),
                metrics=LongText("Include benchmark results for any performance metrics here e.g. accuracy, precision, Recall, ROC-AUC, F1-score."),
                thresholds=LongText("If decision thresholds are used, what are they, and why were those parameters chosen? When the model card is presented in a digital format, a threshold slider should ideally be available to view performance parameters across various decision thresholds."),
                uncertainty=LongText("How are the measurements and estimations of these metrics calculated? For example, this may include standard deviation, variance, confidence intervals, or KL divergence. Details of how these values are approximated should also be included (e.g., average of 5 runs, 10-fold cross-validation)."),
                fairness=LongText("How did the model perform with respect to each factor. Quantitative analyses should be disaggregated, that is, broken down by the chosen factors. Quantitative analyses should provide the results of evaluating the model according to the chosen metrics, providing confidence interval values when possible. Parity on the different metrics across disaggregated population subgroups corresponds to how fairness is often defined. For an example, see figure 2. in https://arxiv.org/pdf/1810.03993.pdf"),
            ),
            safety=DotDict(
                ethics=LongText("Example topics for ethical consideration: Does the training data contain sensitive information? What risks and harms could arise during the use of the model? Which mitigation measures are recommended? Are there particularly problematic use-cases? Did the model go through an ethical assessment procedure?"),
                fairness=LongText("Which definition of fairness have you applied in any phase of setting up the AU system? Did you ensure a quantitative analysis or metrics to measure and test the applied definition of fairness?"),
                risks=LongText("""• Did you define risks, risk metrics and risk levels of the AI system in each specific use case?
o Did you put in place a process to continuously measure and assess risks?
o Did you inform end-users and subjects of existing or potential risks?
• Did you identify the possible threats to the AI system (design faults, technical faults, environmental threats) and the possible consequences?"""),
                security=LongText("Is the AI system certified for cybersecurity (e.g. the certification scheme created by the Cybersecurity Act in Europe)19 or is it compliant with specific security standards? Did you red-team/pentest the system?"),
                caveats=LongText("This section should list additional concerns that were not covered in the previous sections. For example, did the results suggest any further testing? Were there any relevant groups that were not represented in the evaluation dataset? Are there additional recommendations for model use? What are the ideal characteristics of an evaluation dataset for this model?")
            ),
        ))
        self.connector = connector # used by the client - the server does something else and model cards stored there should never set this field
        #VersionControl.__init__(self)

    def __enter__(self):
        assert self.connector, "You need a model card connector to use it as a context"
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()
        return False

    def __del__(self):
        if self.connector:
            assert json.dumps(self.connector.prototype.data) == json.dumps(self.data), \
                "There are uncommitted changes to a model card with a connector. Do one of these:\n * Commit the changes\n * Detach the connector\n * Use the card as a context to auto-commit"

    def detach(self):
        self.connector = None
        return self

    def __getattr__(self, key):
        if key in ["data", "connector"]: return object.__getattribute__(self, key)
        if key in self.data:
            ret = self.data[key]
            return ret.get() if isinstance(ret, Field) else ret
        raise AttributeError

    def __setattr__(self, key, value):
        if key in ["data", "connector"]: return object.__setattr__(self, key, value)
        if key in self.data: self.data[key].set(value)
        return object.__setattr__(self, key, value)

    def is_stable(self):
        return (not self.connector) or json.dumps(self.connector.prototype.data) == json.dumps(self.data)

    def gist(self, assistant):
        assert self.is_stable(), "Cannot obtain a gist while there are uncommited changes"
        if not self.connector:
            card = ModelCard()
            card.data.assign(self.data)
            assistant.refine(card)
        else:
            card = self.connector.create(self)
            assistant.refine(card)
        return card

    def complete(self, assistant, url: str):
        assert self.is_stable(), "Cannot obtain a gist while there are uncommited changes"
        assistant.complete(self, url)
        return self

    def merge(self, data: Union["ModelCard",dict], message: str|None=None):
        if isinstance(data, ModelCard): data = data.data
        assert isinstance(data, dict), "Can only merge with another model card or dct"
        self.data.append(data, message=message)

    def commit(self):
        from aicard.service import converters
        assert self.connector, "The current model card does not have any connector to commit to (either it was not obtained from a connection or it was detached)."
        if json.dumps(self.connector.prototype.data) == json.dumps(self.data):
            self.connector.client.logger.info(f"Nothing to commit")
            return
        result = self.connector.client.put(f"/card/{self.connector.id}", json=converters.dict2dynamic(self.data))
        assert result.status_code == 200, "Failed to commit"
        self.connector.prototype.data.assign(self.data)
        self.connector.client.logger.info(f"Committed card")

    def assign(self, other: "ModelCard"):
        self.data.assign(other.data)

    def summary(self):
        summary = ""
        #if self.data.model.name:
        #    summary += " "+truncate(self.data.model.name.split(" ")[0].split("\n")[0], 50)
        if self.data.model.version:
            summary += " version "+truncate(self.data.model.version, 50)
        return summary[1:] if summary else ""

    def quality(self) -> float:
        nom = 0
        denom = 0
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    denom += 1
                    if value: nom += 1
            else:
                denom += 1
                if dotdict: nom += 1
        return nom/denom

    def to_markdown_card(self):
        card = ModelCard()
        card.title = self.title
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    if isinstance(value, Field): value = value.get()
                    assert isinstance(value, str)
                    card.data[key][field].set(html2text.html2text(value))
        return card

    def to_html_card(self):
        card = ModelCard()
        card.title = self.title
        for key, dotdict in self.data.items():
            if isinstance(dotdict, DotDict):
                for field, value in dotdict.items():
                    if isinstance(value, Field): value = value.get()
                    if not value: value = ""
                    assert isinstance(value, str), f"Field {key} {field} stores type {type(value)} and not a string"
                    # the following line is a trick so that simple strings remain simple strings without <p>
                    value = markdown2.markdown(value, extras=["markdown-in-html", "code-friendly"])
                    if value.startswith("<p>") and value.count("</p>")==1: value = value.strip()[3:-4]
                    card.data[key][field].set(value)
        return card

    def to_markdown(self):
        ret = ""
        card = self.to_markdown_card()
        for key, dotdict in card.data.items():
            if not isinstance(dotdict, DotDict):
                ret += f"# {dotdict.get()}\n"

        # Compute 5-star rating
        quality = self.quality()
        stars = int(round(quality * 5))
        ret += "*completion*".ljust(20) + "⭐" * stars + "☆" * (5 - stars)
        ret += "\n"

        # Add fields
        for key, dotdict in card.data.items():
            if isinstance(dotdict, DotDict):
                segment = ""
                for field, value in dotdict.items():
                    val = value.get().strip()
                    if val and val != "unknown":
                        segment += f"{('*' + field.replace('_', ' ') + '*').ljust(20)} {val}\n\n"

                if segment:
                    ret += f"\n## {key.replace('_', ' ')}\n" + segment
        return ret

    def to_html(self):
        ret = ""
        card = self.to_html_card()
        for key, dotdict in card.data.items():
            if not isinstance(dotdict, DotDict):
                ret += f"<h1>{dotdict.get()}</h1>\n"

        # Compute 5-star rating
        quality = self.quality()
        stars = int(round(quality * 5))
        filled_star = "⭐"
        empty_star = "☆"
        star_html = filled_star * stars + empty_star * (5 - stars)

        ret += (
                f"<div>"
                f"<b>completion</b>".ljust(20)
                + star_html +
                "</div>\n"
        )

        for key, dotdict in card.data.items():
            if isinstance(dotdict, DotDict):
                segment = ""
                for field, value in dotdict.items():
                    val = value.get().strip()
                    if val and str(val) != "unknown":
                        field_label = field.replace("_", " ")
                        segment += f"<p><b>{field_label}</b>: {val}</p>\n"

                if segment:
                    section_title = key.replace("_", " ")
                    ret += f"<h2>{section_title}</h2>\n<div>{segment}</div>\n"

        return f"<div class='card'>{ret}</div>"

    def to_pydantic(self) -> type[BaseModel]:
        fields = {}
        sub_models = {}
        for category, values in self.data.items():
            if not isinstance(values, dict): continue
            sub_model_fields = {}
            for field, value in values.items():
                field_args = {'default': value.get(),'description': value.description}
                if isinstance(value, Options): field_args['enum'] = value.options()
                if isinstance(value, Pattern): field_args['pattern'] = value.pattern()
                sub_model_fields[field] = (str, pydantic_Field(**field_args))
            sub_model = create_model(category, **sub_model_fields)
            sub_models[category] = sub_model
            fields[category] = (sub_model, ...)
        pydantic_model = create_model('card', **fields)
        return pydantic_model

    def json_schema(self):
        schema = self.to_pydantic().model_json_schema()
        return schema

    def to_pydantic_per_category(self) -> dict[str, BaseModel]:
        models = {}
        for category, values in self.data.items():
            if not isinstance(values, dict): continue
            model_fields = {}
            for field, value in values.items():
                field_args = {'default': value.get(),'description': value.description}
                if isinstance(value, Options): field_args['enum'] = value.options()
                if isinstance(value, Pattern): field_args['pattern'] = value.pattern()
                model_fields[field] = (str, pydantic_Field(**field_args))
            model = create_model(category, **model_fields)()
            models[category] = model
        return models

    def json_schema_per_category(self):
        schemas = {category: model.model_json_schema() for category, model in self.to_pydantic_per_category().items()}
        return schemas

    def __str__(self):
        buffer = io.StringIO()
        console = rich.console.Console(file=buffer, force_terminal=True, color_system="truecolor")
        console.print(Markdown(self.to_markdown()))
        return buffer.getvalue().replace("\n\n", "\n")

    def json_dumps(self):
        return json.dumps(self.data)

    def save_json(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps(self.data))

    def load_json(self, filename: str):
        with open(filename, "r") as f:
            self.data.assign(json.loads(f.readline()))

    def save_html(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.to_html())
