import pywikibot
from pywikibot import pagegenerators
import regex as re #use this rather than "re" to avoid the "look-behind requires fixed-width pattern" error

site = pywikibot.Site('zh','wikipedia')
cat = pywikibot.Category(site,'Category:連結格式不正確的條目')
page_to_write = pywikibot.Page(site, u"User:和平奮鬥救地球/MOSIW/links")
gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)

count=0
ilhs = []
ilhn = []

lang_list = 'aa|ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|av|ay|az|azb|ba|bar|bat\-smg|bcl|be|be\-tarask|be\-x\-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk\-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|diq|dsb|dv|dz|ee|egl|eml|el|en|eo|es|et|eu|ext|fa|ff|fi|fiu\-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gd|gl|glk|gn|gom|got|gsw|als|gu|gv|ha|hak|haw|he|hi|hif|ho|hr|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ilo|io|is|it|iu|ja|jp|jam|jbo|jv|ka|kaa|kab|kbd|kg|ki|kj|kk|kl|km|kn|ko|koi|kr|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|lzh|zh\-classical|mai|map\-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|zh\-min\-nan|nap|nb|no|nds|nds\-nl|ne|ne|new|ng|nl|nn|no|nov|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa\-rup|roa\-tara|ru|rue|rup|rw|sa|sah|sc|scn|sco|sd|se|sg|sgs|sh|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|zh\-yue|za|zea|zu'
ilh_search='\[\[\:(?:' + lang_list + ')\:[^\n\r\]]+\]\]'

ilhl_ser = '\[\[\:(' + lang_list + ')'
ilhc_ser = '\[\[\:(?:' + lang_list + ')\:([^\n\r\[\]\|\{\}]+)'

tot_num = len(list(cat.articles(namespaces=0,recurse=True)))
print(tot_num)

for page in gen:
	count+=1
	percentage = 100*count/tot_num
	art_txt = page.text
	ilh_txt = re.findall(ilh_search,art_txt,re.I)
	print(format(percentage, '0.3f'),'%:',page.title())

	for s in ilh_txt:
		if s in ilhs:
			ilhn[ilhs.index(s)]+=1
		else:
			ilhs.append(s)
			ilhn.append(1)

pct = 0
for i in range(len(ilhn)):
	if(i>=0.01*pct*len(ilhn)): 
		print(pct,'%')
		pct+=1
	for j in range(len(ilhn)-i-1):
		if ilhn[j] < ilhn[j+1]:
			ilhn[j], ilhn[j+1] = ilhn[j+1], ilhn[j]
			ilhs[j], ilhs[j+1] = ilhs[j+1], ilhs[j]

writestr = '[[:Category:連結格式不正確的條目]]當中前1,000高使用量之不合規跨語言連結\n\n'
writestr += '最後更新時間：~~~~~\n\n'
writestr += '{| class="wikitable sortable"\n! 連結 !! 使用量 !! 對應語言頁面是否存在 !! 是否已有對應中文頁面 !! 對應中文頁面 \n'

pct = 0
for i in range(len(ilhn)):
	if(i>=0.01*pct*len(ilhn)): 
		print(pct,'%')
		pct+=1

	ilh_lang = re.findall(ilhl_ser,ilhs[i],re.I)
	ilh_orl = re.findall(ilhc_ser,ilhs[i],re.I)

	orlexists = False
	zhtitle = "無"
	haszh = False

	nsn = 0
	if len(ilh_orl)>0: 
		nsn += len(re.findall('^#',ilh_orl[0],re.I))
		nsn += len(re.findall('^Special\:',ilh_orl[0],re.I))
		nsn += len(re.findall('^特別\:',ilh_orl[0],re.I))

	else: nsn=0
	
	if len(ilh_orl)>0 and nsn==0:
		if ilh_lang[0].lower()=='jp': ilh_lang[0]='ja'
		elif ilh_lang[0].lower()=='nb': ilh_lang[0]='no'
		elif ilh_lang[0].lower()=='be-x-old': ilh_lang[0]='be-tarask'
		elif ilh_lang[0].lower()=='lzh': ilh_lang[0]='zh-classical'
		site_orl = pywikibot.Site(ilh_lang[0].lower(),'wikipedia')
		page_orl = pywikibot.Page(site_orl,ilh_orl[0])
		if page_orl.exists():
			orlexists = True
			langlinks = page_orl.langlinks()
			
			for ll in langlinks:
				if(ll.site==site):
					zhtitle = '[[' + ll.title + ']]'
					haszh = True
					break

	writestr += '|-\n|<nowiki>' + ilhs[i] + '</nowiki>||' + str(ilhn[i]) + '||' + str(orlexists) + '||' + str(haszh) + '|| ' + zhtitle + '\n'
	#print(ilh_lang[0])
	#print(ilh_orl[0])
	#print(orlexists)
	#print(haszh)
	#print(zhtitle)
	#print('=====')
	if i>1000: break

writestr += '|}'
page_to_write.text = writestr
page_to_write.save(u"使用[[mw:Manual:Pywikibot/zh|Pywikibot]]更新數據")
print('Done')