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
obcine_html = osnovne_definicije.vsebina_datoteke('podatki/index.html')
stranke_html = osnovne_definicije.vsebina_datoteke('podatki/2010-2014.html')
brez_strank_html = osnovne_definicije.vsebina_datoteke('podatki/2006-2010.html')
stranke1_html = osnovne_definicije.vsebina_datoteke('podatki/2002-2006.html')
stranke2_html = osnovne_definicije.vsebina_datoteke('podatki/1998-2002.html')
stranke3_html = osnovne_definicije.vsebina_datoteke('podatki/1994-1998.html')

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
    podatki_obcine.append({'link': link, 'ime': ime, 'zupan': zupan, 'prebivalci': prebivalci, 'povrsina': povrsina, 'email': email})
    osnovne_definicije.zapisi_tabelo(podatki_obcine, ['ime', 'zupan', 'email', 'povrsina', 'prebivalci', 'link'], 'csv-datoteke/index.csv')

def vrni_podatke_wiki(html_besedilo):
    """
    Dela za Wikipedijo.
    """
    stranke_2014 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=".*?">(.*?)</a></td>""" 

    stranke_2006 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=".*?">(.*?)</a></td>"""

    stranke_2002 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=".*?">(.*?)</a></td>"""

    stranke_1998 = r"""<td><a href="/wiki/.*?" title=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=.*?>(.*?)</a></td>""" + \
                   r"""<td><a href=".*?">(.*?)</a></td>"""
                       

    rezultat = re.findall(stranke_2006, html_besedilo)
    return rezultat
    
podatki = vrni_podatke_wiki(stranke_html)
podatki_obcine = []
for _, _, obcina, zupan, predlagatelj in podatki:
    podatki_obcine.append({'obcina': obcina, 'zupan': zupan, 'predlagatelj': predlagatelj})
    osnovne_definicije.zapisi_tabelo(podatki_obcine, ['obcina', 'zupan', 'predlagatelj'], 'csv-datoteke/2010-2014.csv')
 
def vrni_podatke_wiki_brez_stranke(html_besedilo):
    """
    Dela za Wikipedijo za 2006 - 2010.
    """
    vzorec = r"""<td><a href="/wiki.*?" title=.*?>(.*?)</a></td>""" + \
             r"""<td><a href=".*?" .*?">(.*?)</a></td>"""
            
    rezultat = re.findall(vzorec, html_besedilo)
    return rezultat

podatki = vrni_podatke_wiki_brez_stranke(brez_strank_html)
podatki_obcine = []
for _, _, obcina, zupan in podatki:
    podatki_obcine.append({'obcina': obcina, 'zupan': zupan})
    osnovne_definicije.zapisi_tabelo(podatki_obcine, ['obcina', 'zupan'], 'csv-datoteke/2006-2010.csv')

#def vrni_podatke_naselja(html_besedilo):
#naselja = r"""Število naselij</a></th><td>(.*?)</td></tr><tr><th""" #št.naselij
 #       r"""Št. prebivalcev</a></th><td>(.*?)</td></tr><tr><th title="Statistični podatki">""" # št.prebivalcev
  #      r"""Površina \(km2\)</a></th><td>(.*?)</td></tr>""" #površina
        
              


    
