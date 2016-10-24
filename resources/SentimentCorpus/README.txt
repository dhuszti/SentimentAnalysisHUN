OpinHuBank 2013-01-06

OpinHuBank is a human-annotated corpus to aid the research of opinion mining and sentiment analysis in Hungarian. It consists of 10,000 sentences containing person names (identified with the huntag NER tool) from major Hungarian news sites and blogs. Each entity occurrence was tagged by 5 human annotators for sentiment polarity in its sentence (neutral, positive or negative).
The corpus is available for download via the META-SHARE network (http://www.meta-share.eu/), or you can also download it from https://sites.google.com/site/mmihaltz/resources.
Please cite the following paper when referencing OpinHuBank in your work:

Miháltz Márton: OpinHuBank: szabadon hozzáférhetõ annotált korpusz magyar nyelvû véleményelemzéshez. In Tanács Attila, Vincze Veronika (szerk.): IX. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2013), SZTE, Szeged, 2013, pp. 343-345.

For more information, please read the paper (Hungarian): https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxtbWloYWx0enxneDo3NjIxOGE0NjUzOWY2OWVm

The annotated corpus data is available in 2 formats:

OpinHuBank_20130106.xls: MS Excel 97/2000/XP

OpinHuBank_20130106.csv: Text CSV (encoding: ISO-8859-2, field delimiter: ',', text delimiter: '"')

Both files have the following columns:

ID: id of the annotation unit	
START: starting positions of the named entity in the sentence (index of its first token)
LEN: length (number of tokens) of the entity
Entity: the named entity
Sentence: the sentence containing the entity
URL: original location of text containing sentence
Annot1,...,Annot5: judgements of entity's sentiment polarity in the sentence (0: neutral, 1: positive, -1: negative) by the 5 human annotators

For more information, contact:
Márton Miháltz
mihaltz.marton@nytud.mta.hu
