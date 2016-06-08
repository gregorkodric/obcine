import osnovne_definicije
import re
import html

osnovne_definicije.pripravi_imenik('podatki')
osnovne_definicije.shrani('https://skupnostobcin.si/obcine/', 'podatki/index.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%282010-2014%29','podatki/index.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%282006-2010%29','podatki/index.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%282002-2006%29','podatki/index.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%281998-2002%29','9podatki/index.html')
osnovne_definicije.shrani('https://sl.wikipedia.org/wiki/Seznam_%C5%BEupanov_ob%C4%8Din_v_Sloveniji_%281994-1998%29','podatki/index.html')
obcine_html = osnovne_definicije.vsebina_datoteke('podatki/index.html')

def vrni_podatke(html_besedilo):
    vzorec = r"""<tr id="(.*?)" data-idob="(.*?)" data-oblink="(.*?)" class=".*?">\s*<th>""" + \
            r"""\s*<a href=".*?" rel="bookmark">(.*?)</a>\s*</th>\s*<td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>""" + \
            r"""\s*<td><a href=".*?">(.*?)</a></td>\s*</tr>"""

    #stranke = r"""<td><a href=".*?" title=".*?">(.*?)<\/a><\/td>"""  ime občine
             #r"""<td><a href=".*?" title=".*?" class=".*?">(.*?)<\/a><\/td>"""  župan
             #r"""<td><a href=".*?" class="new" title=".*?">(.*?)<\/a><\/td>"""  ime stranke
    rezultat = re.findall(vzorec, html_besedilo)
    return rezultat

podatki = vrni_podatke(obcine_html)
for _, _, link, ime, zupan, prebivalci, povrsina, email in podatki:
    email = html.unescape(email)
    print(link, ime, zupan, prebivalci, povrsina, email)
print(len(podatki))
