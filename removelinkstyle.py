import pywikibot
from pywikibot import pagegenerators
import regex as re #use this rather than "re" to avoid the "look-behind requires fixed-width pattern" error

site = pywikibot.Site('zh','wikipedia')
cat = pywikibot.Category(site,'Category:連結格式不正確的條目')
gen = pagegenerators.CategorizedPageGenerator(cat, recurse=True)

ilh='(?<!\{\{(Advtranslation|Plant\-translation|Translate|Translating|Translation[ _]+WIP|Translation|Trans|Tran|Voltranslation|Wptranslation|正在翻(譯|译)|(翻)?(譯|译)(中)?)[^\}]*)\[\[\:(w|aa|ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|av|ay|az|azb|ba|bar|bat-smg|bcl|be|be-tarask|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|diq|dsb|dv|dz|ee|egl|eml|el|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gd|gl|glk|gn|gom|got|gsw|als|gu|gv|ha|hak|haw|he|hi|hif|ho|hr|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ilo|io|is|it|iu|ja|jp|jam|jbo|jv|ka|kaa|kab|kbd|kg|ki|kj|kk|kl|km|kn|ko|koi|kr|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|lzh|zh-classical|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|zh-min-nan|nap|nb|no|nds|nds-nl|ne|ne|new|ng|nl|nn|no|nov|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|rw|sa|sah|sc|scn|sco|sd|se|sg|sgs|sh|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|zh-yue|za|zea|zu)\:(?!(wiktionary|wikt|wikinews|n|wikibooks|b|wikiquote|q|wikisource|s|oldwikisource|species|wikispecies|wikiversity|v|betawikiversity|wikimedia|foundation|wmf|wikivoyage|voy|commons|c|meta|metawikipedia|m|strategy|incubator|mediawikiwiki|mw|mediawiki|quality|otrswiki|otrs|ticket|phabricator|bugzilla|mediazilla|phab|nost|testwiki|wikidata|d|outreach|outreachwiki|toollabs|wikitech|dbdump|download|gerrit|mail|mailarchive|rev|spcom|sulutil|svn|tools|tswiki|wm2016|wm2017|wmania|User|Wikipedia|MediaWiki|File|Image|WP|Project|Template|Help|Special|U|利用者)\:)|(?<=\r|\n)(\=){2,}.*\[\[.*\]\].*(\=){2,}|\[\[(JP|JA|EN)\:\:'

ls_t='\{\{Link style\|time=\d{4}\-\d{2}\-\d{2}T\d{2}\:\d{2}\:\d{2}\+00:00\}\}'

count = 0

tot_num = len(list(cat.articles(namespaces=0,recurse=True)))
print(tot_num)

for page in gen:
	count+=1

	art_txt = page.text
	ilh_num = len(re.findall(ilh,art_txt,re.I))
	if(ilh_num>0): continue

	new_art_txt = re.sub(ls_t+'\n','',art_txt,flags=re.I)
	new_art_txt = re.sub(ls_t,'',new_art_txt,flags=re.I)

	page.text = new_art_txt
	percentage = 100*count/tot_num

	print(format(percentage, '0.3f'),'%:',page.title(),'has',ilh_num,' interlang links and has removed {{Link Style}}.')

	page.save(u"機器人：摘掉已符合[[WP:MOSIW|跨語言連結規範]]之條目Link Style標記")


print('Done')