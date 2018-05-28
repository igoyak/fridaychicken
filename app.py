from flask import Flask
from datetime import datetime
import requests
import re
import pytz
from lxml import html, etree
import sys
import traceback
#from pprint import pprint

app = Flask(__name__)


def friday_lunch():
    a = requests.get('https://www.himasali.com/lounaslista/', verify=False)
    tree = html.fromstring(a.content)
    #finnish_list = tree.xpath('//div[@class="container"]//div[@class="wpb_wrapper"]//div[@class="cv_row wpb_row vc_inner vc_row-fluid"]')
    mypath = '//div[@class="container"]/div[@class="row"]/div[@class="wpb_column vc_column_container vc_col-sm-12"]//p' #/div[@class="vc_column-inner"]'
    dishes = tree.xpath(mypath)
    fi_friday = dishes[4]
    #print(len(fi_friday))
    print(etree.tostring(fi_friday))
    print(etree.tostring(fi_friday[4]))
    assert 'Wokki' in etree.tostring(fi_friday[4]).decode('utf-8')
    print('wokki found')
    print(len(fi_friday[3]))
    maybechicken = etree.tostring(fi_friday[3]).decode('utf-8')[6:]
    print('maybechicken: ', maybechicken)
    assert 'kalalounas:' in maybechicken
    print('liha/kala found')
    maybechicken = maybechicken.split('kalalounas:')[1]
    #return maybechicken[16:]
    print(maybechicken)
    return maybechicken
    #items = fi_friday.split('<br/>')
    #pprint(items)

    #print(len(first_container))
    #print(first_container)
    #print(etree.tostring(first_container))
    #chicken_list = first_container.xpath('/p')
    #for x in first_container:
        #print(etree.tostring(x))
    #print(etree.tostring(finnish_list))
    return 'foo'
    text = a.text
    a = text.split('Huom! Muu')[0]
    b = a.split('kalalounas:')[-1]
    c = b.split('<br />')[0]
    return c


with open('html/index.html') as f:
    htmltempl = f.read()

with open('html/style.css') as f:
    css = f.read()


@app.route('/')
def homepage():
    error_text = ''
    try:
        lunch = friday_lunch()
        is_kana = bool(re.compile('(kana|broiler)', re.IGNORECASE).search(lunch))
        print(lunch)
        verdict = 'Yes!' if is_kana else 'No :('
    except Exception as e:
        error_text = traceback.format_exc()
        print(error_text)
        is_kana = False
        lunch = ''
        verdict = 'The scraper broke :('
    finally:
        sys.stdout.flush()

    replace = {'dish': lunch,
               'verdict': verdict,
               'lastcheck': datetime.now(pytz.timezone('Europe/Helsinki')).strftime("%A, %d %b %Y %H:%M"),
               'style': 'yes' if is_kana else 'no',
               'css': css,
               'error': error_text
               }
    return htmltempl.format(**replace)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)
