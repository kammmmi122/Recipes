#!/bin/bash

asciidoctor -a docinfo=shared --backend=html5 ./../*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy ./../Przepisy/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Przetwory ./../Przepisy/Przetwory/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Przystawki ./../Przepisy/Przystawki/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Makarony ./../Przepisy/Makarony/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Desery ./../Przepisy/Desery/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Dania_glowne ./../Przepisy/Dania_glowne/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Zupy ./../Przepisy/Zupy/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./../Przepisy/Salatki ./../Przepisy/Salatki/*.adoc
