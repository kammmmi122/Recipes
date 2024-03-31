#!/bin/bash

asciidoctor -a docinfo=shared --backend=html5 ./*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./Przepisy/* ./Przepisy/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./Przepisy/Przetwory ./Przepisy/Przetwory/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./Przepisy/Desery ./Przepisy/Desery/*.adoc
asciidoctor -a docinfo=shared --backend=html5 -D ./Przepisy/Dania_glowne ./Przepisy/Dania_glowne/*.adoc