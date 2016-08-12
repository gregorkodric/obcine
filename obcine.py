import osnovne_definicije
import re
import html

osnovne_definicije.pripravi_imenik('podatki')
osnovne_definicije.shrani('https://skupnostobcin.si/obcine/', 'podatki/index.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%282010-2014%29','podatki/2010-2014.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%282006-2010%29','podatki/2006-2010.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%282002-2006%29','podatki/2002-2006.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%281998-2002%29','podatki/1998-2002.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%281994-1998%29','podatki/1994-1998.html')
osnovne_definicije.shrani('https://skupnostobcin.si/podatki/statisticni-podatki/', 'podatki/naselja.html')

obcine_html = osnovne_definicije.vsebina_datoteke('podatki/index.html')
stranke_html = osnovne_definicije.vsebina_datoteke('podatki/2010-2014.html')
brez_strank_html = osnovne_definicije.vsebina_datoteke('podatki/2006-2010.html')
stranke1_html = osnovne_definicije.vsebina_datoteke('podatki/2002-2006.html')
stranke2_html = osnovne_definicije.vsebina_datoteke('podatki/1998-2002.html')
stranke3_html = osnovne_definicije.vsebina_datoteke('podatki/1994-1998.html')
naselja_html = osnovne_definicije.vsebina_datoteke('podatki/naselja.html')

def vrni_podatke(html_besedilo):
    """
    Dela za https://skupnostobcin.si/obcine/.
    """
    vzorec = r"""<tr id="(.*?)" data-idob="(.*?)" data-oblink="(.*?)" class=".*?">\s*<th>""" + \
            r"""\s*<a href=".*?" rel="bookmark">(.*?)</a>\s*</th>\s*<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>""" + \
            r"""\s*<td><a href=".*?">(.*?)</a></td>\s*</tr>"""

    rezultat = re.findall(vzorec, html_besedilo)
    return rezultat

podatki = vrni_podatke(obcine_html)
podatki_obcine = []

for _, _, link, ime, zupan, prebivalci, povrsina, email in podatki:
    email = html.unescape(email)
    ime = html.unescape(ime)
    podatki_obcine.append({'link': link,
                           'ime': ime,
                           'zupan': zupan,
                           'prebivalci': prebivalci,
                           'povrsina': povrsina,
                           'email': email})

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                 ['ime', 'zupan', 'email', 'povrsina', 'prebivalci', 'link'],
                                 'csv-datoteke/index.csv')


def vrni_podatke_wiki_2014(html_besedilo):
    """
    Dela za Wikipedijo.
    """
    stranke_2014_old = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                       r"""<td><a href=.*?>(.*?)</a></td>\s*""" + \
                       r"""<td>(<a href=".*?" title=".*?">(.*?)</a>|(.*?))</td>""" 
    stranke_2014 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                   r"""<td>(.*?)</td>\s*""" + \
                   r"""<td>(.*?)</td>""" 
               
    rezultat = re.findall(stranke_2014, html_besedilo, flags=re.DOTALL)
    # print('***')
    # print(rezultat)
    # print('***')
    return rezultat

def ocisti_zupana(niz):
    ime_zupana = r"<a .*?>(.*?)</a>"
    if niz.startswith('<a'):
        return re.match(ime_zupana, niz).group(1)
    return niz

def ocisti_stranke(niz):
    predlagatelji = [x.strip() for x in niz.split('<br />')]
    pred = []
    for p in predlagatelji:
        ime_stranke = r"<a .*?>(.*?)</a>"
        if p.startswith('<a'):
            pred.append(re.match(ime_stranke, p).group(1))
        else:
            pred.append(p)
    return ';'.join(pred)

podatki = vrni_podatke_wiki_2014(stranke_html)
podatki_obcine = []
for obcina, zupan, predlagatelj in podatki:
    podatki_obcine.append({'obcina': obcina,
                           'zupan': ocisti_zupana(zupan),
                           'predlagatelj': ocisti_stranke(predlagatelj)})

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                 ['obcina', 'zupan', 'predlagatelj'],
                                 'csv-datoteke/2010-2014.csv')
# print(podatki_obcine)


def vrni_podatke_wiki_2006(html_besedilo):

    stranke_2006_old = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                       r"""<td><a href=.*?>(.*?)</a></td>\s*""" + \
                       r"""<td>(<a href=".*?" title=".*?">(.*?)</a>|(.*?))</td>""" 

    stranke_2006 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                   r"""<td>(.*?)</td>\s*""" + \
                   r"""<td>(.*?)</td>"""

    rezultat = re.findall(stranke_2006, html_besedilo, flags=re.DOTALL)

    return rezultat

def ocisti_zupana(niz):
    ime_zupana = r"<a .*?>(.*?)</a>"
    if niz.startswith('<a'):
        return re.match(ime_zupana, niz).group(1)
    return niz

def ocisti_stranke(niz):
    predlagatelji = [x.strip() for x in niz.split('<br />')]
    pred = []
    for p in predlagatelji:
        ime_stranke = r"<a .*?>(.*?)</a>"
        if p.startswith('<a'):
            pred.append(re.match(ime_stranke, p).group(1))
        else:
            pred.append(p)
    return ';'.join(pred)
    
podatki = vrni_podatke_wiki_2006(stranke1_html)
podatki_obcine = []
for obcina, zupan, predlagatelj in podatki:
    podatki_obcine.append({'obcina': obcina,
                           'zupan': ocisti_zupana(zupan),
                           'predlagatelj': ocisti_stranke(predlagatelj)})

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                 ['obcina', 'zupan', 'predlagatelj'],
                                 'csv-datoteke/2002-2006.csv')

    


def vrni_podatke_wiki_2002(html_besedilo):

    stranke_2002_old = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                       r"""<td><a href=.*?>(.*?)</a></td>\s*""" + \
                       r"""<td>(<a href=".*?" title=".*?">(.*?)</a>|(.*?))</td>""" 

    stranke_2002 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                   r"""<td>(.*?)</td>\s*""" + \
                   r"""<td>(.*?)</td>"""

    rezultat = re.findall(stranke_2002, html_besedilo, flags=re.DOTALL)
    return rezultat

def ocisti_zupana(niz):
    ime_zupana = r"<a .*?>(.*?)</a>"
    if niz.startswith('<a'):
        return re.match(ime_zupana, niz).group(1)
    return niz

def ocisti_stranke(niz):
    predlagatelji = [x.strip() for x in niz.split('<br />')]
    pred = []
    for p in predlagatelji:
        ime_stranke = r"<a .*?>(.*?)</a>"
        if p.startswith('<a'):
            pred.append(re.match(ime_stranke, p).group(1))
        else:
            pred.append(p)
    return ';'.join(pred)
    
    
podatki = vrni_podatke_wiki_2002(stranke2_html)
podatki_obcine = []
for obcina, zupan, predlagatelj in podatki:
    podatki_obcine.append({'obcina': obcina,
                           'zupan': ocisti_zupana(zupan),
                           'predlagatelj': ocisti_stranke(predlagatelj)})

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                 ['obcina', 'zupan', 'predlagatelj'],
                                 'csv-datoteke/1998-2002.csv')



def vrni_podatke_wiki_1998(html_besedilo):

    stranke_2008_old = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>\s*""" + \
                   r"""<td><a href=.*?>(.*?)</a></td>\s*""" + \
                   r"""<td>(<a href=".*?" title=".*?">(.*?)</a>|(.*?))</td>""" 

    stranke_1998 = r"""<td><a .*?>(.*?)</a></td>\s*""" + \
                   r"""<td>(.*?)</td>\s*""" + \
                   r"""<td>(.*?)</td>"""

    rezultat = re.findall(stranke_1998, html_besedilo, flags=re.DOTALL)
    return rezultat

def ocisti_zupana(niz):
    ime_zupana = r"<a .*?>(.*?)</a>"
    if niz.startswith('<a'):
        return re.match(ime_zupana, niz).group(1)
    return niz

def ocisti_stranke(niz):
    predlagatelji = [x.strip() for x in niz.split('<br />')]
    pred = []
    for p in predlagatelji:
        ime_stranke = r"<a .*?>(.*?)</a>"
        if p.startswith('<a'):
            pred.append(re.match(ime_stranke, p).group(1))
        else:
            pred.append(p)
    return ';'.join(pred)



podatki = vrni_podatke_wiki_1998(stranke3_html)
podatki_obcine = []
for obcina, zupan, predlagatelj in podatki:
    podatki_obcine.append({'obcina': obcina,
                           'zupan': ocisti_zupana(zupan),
                           'predlagatelj': ocisti_stranke(predlagatelj)})

"""
for x in podatki_obcine:
    print(x)
"""

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                ['obcina', 'zupan', 'predlagatelj'],
                                 'csv-datoteke/1994-1998.csv')
    
        


    
def vrni_podatke_wiki_brez_stranke(html_besedilo):
    """
    Dela za Wikipedijo za 2006 - 2010.
    """
    brez_stranke = r"""<td><a href="/wiki.*?" title=.*?>(.*?)</a></td>\s*""" + \
             r"""<td><a href=".*?" .*?">(.*?)</a></td>"""
            
    rezultat = re.findall(brez_stranke, html_besedilo)
    return rezultat

podatki = vrni_podatke_wiki_brez_stranke(brez_strank_html)
podatki_obcine = []
for obcina, zupan in podatki:
    podatki_obcine.append({'obcina': obcina,
                           'zupan': zupan})

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                 ['obcina', 'zupan'],
                                 'csv-datoteke/2006-2010.csv')

    #def vrni_podatke_naselja(html_besedilo):
    #naselja = r"""Število naselij</a></th><td>(.*?)</td></tr><tr><th""" #št.naselij
     #       r"""Št. prebivalcev</a></th><td>(.*?)</td></tr><tr><th title="Statistični podatki">""" # št.prebivalcev
      #      r"""Površina \(km2\)</a></th><td>(.*?)</td></tr>""" #površina
            
                  
def vrni_podatke_naselja(html_besedilo):
    naselje = r"""<tr id="\d*"( class="alternate")?>(.*?)</tr>"""

    naselje2 = r"""<th><a href=".*?">(.*?)</a></th>""" + \
            r"""<td>(.*?)</td>""" + \
            r"""<td class="column-columnname">(\d*)</td>""" + \
            r"""<td class="column-columnname">(\d*)</td>""" + \
            r"""<td class="column-columnname">(\d*)</td>"""

    rezultat = re.findall(naselje, html_besedilo)
    rezultat2 = []
    for _, vsebina in rezultat:
        m = re.search(naselje2, vsebina)
        rezultat2.append((m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
    return rezultat2

print('***')
podatki = vrni_podatke_naselja(naselja_html)
print('###')
podatki_obcine = []
for obcina, regija, naselje, prebivalci, povrsina in podatki:
    podatki_obcine.append({'obcina': obcina,
                            'regija': regija,
                           'naselje': naselje,
                           'prebivalci': prebivalci,
                           'povrsina': povrsina})

osnovne_definicije.zapisi_tabelo(podatki_obcine,
                                 ['obcina', 'regija', 'naselje', 'prebivalci', 'povrsina'],
                                 'csv-datoteke/naselja.csv')
    
"""
<tr id="1">
<th><a href="https://skupnostobcin.si/obcina/ajdovscina/">Ajdovščina</a></th>
<td>GORIŠKA STATISTIČNA REGIJA</td>
<td class="column-columnname">45</td>
<td class="column-columnname">18959</td>
<td class="column-columnname">245</td>
</tr>

<tr id="213" class="alternate">
<th><a href="https://skupnostobcin.si/obcina/ankaran/">Ankaran</a></th>
<td>OBALNO-KRAŠKA STATISTIČNA REGIJA</td>
<td class="column-columnname">1</td>
<td class="column-columnname">3219</td>
<td class="column-columnname">8</td>
</tr>
"""
