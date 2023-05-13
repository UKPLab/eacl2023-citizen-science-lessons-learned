# Lessons Learned from a Citizen Science Project for Natural Language Processing

This repository includes code that we used for the experiments in our EACL 2023 paper:

```
Lessons Learned from a Citizen Science Project for Natural Language Processing
Jan-Christoph Klie, Ji-Ung Lee, Kevin Stowe, Gözde Şahin, Nafise Sadat Moosavi, Luke Bates, Dominic Petrak, Richard Eckart De Castilho, Iryna Gurevych
```

> **Abstract:** Many Natural Language Processing (NLP) systems use annotated corpora for training and evaluation. 
> However, labeled data is often costly to obtain and scaling annotation projects is difficult, which is why annotation 
> tasks are often outsourced to paid crowdworkers. Citizen Science is an alternative to crowdsourcing that is relatively 
> unexplored in the context of NLP. To investigate whether and how well Citizen Science can be applied in this setting,
> we conduct an exploratory study into engaging different groups of volunteers in Citizen Science for NLP by
> re-annotating parts of a pre-existing crowdsourced dataset. Our results show that this can yield high-quality
> annotations and at- tract motivated volunteers, but also requires considering factors such as scalability, 
> participation over time, and legal and ethical issues. We summarize lessons learned in the form of guidelines and 
> provide our code and data to aid future work on Citizen Science.

Contact person: [Jan-Christoph Klie](mailto:ukp@mrklie.com)

https://www.ukp.tu-darmstadt.de
https://www.tu-darmstadt.de

Don't hesitate to report an issue if something is broken (and it shouldn't be) or if you have further questions.

> ⚠️ **This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.** 

Please use the following citation when using our software:

```bibtex
@inproceedings{klie-etal-2023-lessons,
    title = "Lessons Learned from a Citizen Science Project for Natural Language Processing",
    author = {Klie, Jan-Christoph  and
      Lee, Ji-Ung  and
      Stowe, Kevin  and
      {\c{S}}ahin, G{\"o}zde  and
      Moosavi, Nafise Sadat  and
      Bates, Luke  and
      Petrak, Dominic  and
      Eckart De Castilho, Richard  and
      Gurevych, Iryna},
    booktitle = "Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics",
    month = may,
    year = "2023",
    address = "Dubrovnik, Croatia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.eacl-main.261",
    pages = "3594--3608",
    abstract = "Many Natural Language Processing (NLP) systems use annotated corpora for training and evaluation. However, labeled data is often costly to obtain and scaling annotation projects is difficult, which is why annotation tasks are often outsourced to paid crowdworkers. Citizen Science is an alternative to crowdsourcing that is relatively unexplored in the context of NLP. To investigate whether and how well Citizen Science can be applied in this setting, we conduct an exploratory study into engaging different groups of volunteers in Citizen Science for NLP by re-annotating parts of a pre-existing crowdsourced dataset. Our results show that this can yield high-quality annotations and at- tract motivated volunteers, but also requires considering factors such as scalability, participation over time, and legal and ethical issues. We summarize lessons learned in the form of guidelines and provide our code and data to aid future work on Citizen Science.",
}
```

## Webapp

Basic implementation of the webapp linking to specific annotation projects.
The app allows you to create an own account and add specific annotation tasks. 

### Installation

### Usage

1. Adding a new account:
   - Go on http://127.0.0.1:5000/register 
   - Add username and password (private)
   - Add your name, address, and email (will be displayed in the informed consent form)

2. Creating a new annotation task:
   - After you log in (http://127.0.0.1:5000/login) using your credentials go on http://127.0.0.1:5000/create_task
   - You are now asked to enter some basic information about the collected data.
   - You can include additional checkboxes such as a timestamp on top of the page ('Add Data Type')
   - Most of the text fields are pre-filled, but also required. Only the questionnaire is optional.

3. To participate in a study (no login required) go on 'Select Study'
   - Select a task. You will be then guided throughout the informed consent form. 
   - The link to the study will be provided at the end ('Start the Annotation Task' button)


