import pywikibot
from pywikibot import pagegenerators
from urllib.request import urlopen
import urllib.parse
import regex as re #use this rather than "re" to avoid the "look-behind requires fixed-width pattern" error

site = pywikibot.Site('zh','wikipedia')
cat = pywikibot.Category(site,'Category:連結格式不正確的條目')
page_to_write = pywikibot.Page(site, u"User:和平奮鬥救地球/MOSIW")
gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)

ilh='(?<!\{\{(Advtranslation|Plant\-translation|Translate|Translating|Translation[ _]+WIP|Translation|Trans|Tran|Voltranslation|Wptranslation|正在翻(譯|译)|(翻)?(譯|译)(中)?)[^\}]*)\[\[\:(aa|ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|av|ay|az|azb|ba|bar|bat-smg|bcl|be|be-tarask|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|diq|dsb|dv|dz|ee|egl|eml|el|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gd|gl|glk|gn|gom|got|gsw|als|gu|gv|ha|hak|haw|he|hi|hif|ho|hr|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ilo|io|is|it|iu|ja|jp|jam|jbo|jv|ka|kaa|kab|kbd|kg|ki|kj|kk|kl|km|kn|ko|koi|kr|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|lzh|zh-classical|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|zh-min-nan|nap|nb|no|nds|nds-nl|ne|ne|new|ng|nl|nn|no|nov|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|rw|sa|sah|sc|scn|sco|sd|se|sg|sgs|sh|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|zh-yue|za|zea|zu)\:(?!(wiktionary|wikt|wikinews|n|wikibooks|b|wikiquote|q|wikisource|s|oldwikisource|species|wikispecies|wikiversity|v|betawikiversity|wikimedia|foundation|wmf|wikivoyage|voy|commons|c|meta|metawikipedia|m|strategy|incubator|mediawikiwiki|mw|mediawiki|quality|otrswiki|otrs|ticket|phabricator|bugzilla|mediazilla|phab|nost|testwiki|wikidata|d|outreach|outreachwiki|toollabs|wikitech|dbdump|download|gerrit|mail|mailarchive|rev|spcom|sulutil|svn|tools|tswiki|wm2016|wm2017|wmania|User|Wikipedia|MediaWiki|File|Image|WP|Project|Template|Help|Special|U|利用者)\:)|\[\[(JP|JA|EN)\:\:'

viewcount = 0

arts = []
views = []
ilh_count = []
edit_num = []
page_size = []

count = 0

html_start = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/zh.wikipedia/all-access/user/"
html_end = "/monthly/2020100100/2020110100"

tot_num = len(list(cat.articles(namespaces=0,recurse=True)))
print(tot_num)

for page in gen:
	count+=1
	percentage = 100*count/tot_num
	art_name = page.title()
	html_url = html_start + urllib.parse.quote(art_name).replace('/','%2F') + html_end
	try:
		urlopen(html_url)
	except:
		continue
	html = urlopen(html_url).read()
	strhtml = str(html)
	viewcount = strhtml[strhtml.find('views')+7:-4]

	if(int(viewcount)<1000): continue

	art_txt = page.text
	ilh_num = len(re.findall(ilh,art_txt,re.I))

	print(format(percentage, '0.3f'),'%:',art_name,viewcount,ilh_num,page.revision_count(),len(page.text.encode("utf8")))

	arts.append(art_name)
	views.append(int(viewcount))
	ilh_count.append(ilh_num)
	edit_num.append(page.revision_count())
	page_size.append(len(page.text.encode("utf8")))

for i in range(len(views)):
	for j in range(len(views)-i-1):
		if views[j]<views[j+1]:
			views[j], views[j+1] = views[j+1], views[j]
			arts[j], arts[j+1] = arts[j+1], arts[j]
			ilh_count[j], ilh_count[j+1] = ilh_count[j+1], ilh_count[j]
			edit_num[j], edit_num[j+1] = edit_num[j+1], edit_num[j]
			page_size[j], page_size[j+1] = page_size[j+1], page_size[j]

writestr = '[[:Category:連結格式不正確的條目]]當中前1,000高瀏覽量（2020年10月份數據）之條目\n\n'
writestr += '最後更新時間：~~~~~\n\n'
writestr += '{| class="wikitable sortable"\n! 條目名 !! 瀏覽量 !! 不合規跨語言連結總數（粗估） !! 頁面編輯次數 !! 頁面長度（位元組）\n'


for i in range(len(views)):
	if i>=1000: break
	print(arts[i],views[i])
	writestr += '|-\n|[[' + arts[i] + ']]||' + str(views[i]) + '||' + str(ilh_count[i]) + '||' + str(edit_num[i]) + '||' + str(page_size[i]) + '\n'
	
writestr += '|}'

page_to_write.text = writestr
page_to_write.save(u"使用[[mw:Manual:Pywikibot/zh|Pywikibot]]更新數據")
print('Done')