import pywikibot
from pywikibot import pagegenerators
import regex as re #use this rather than "re" to avoid the "look-behind requires fixed-width pattern" error

site = pywikibot.Site('zh','wikipedia')
ilh_search0='insource:/\[\[\:([A-Za-z\-]{2,})\:/i'
ilh_search='\[\[\:(aa|ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|av|ay|az|azb|ba|bar|bat-smg|bcl|be|be-tarask|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|diq|dsb|dv|dz|ee|egl|eml|el|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gd|gl|glk|gn|gom|got|gsw|als|gu|gv|ha|hak|haw|he|hi|hif|ho|hr|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ilo|io|is|it|iu|ja|jp|jam|jbo|jv|ka|kaa|kab|kbd|kg|ki|kj|kk|kl|km|kn|ko|koi|kr|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|lzh|zh-classical|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|zh-min-nan|nap|nb|no|nds|nds-nl|ne|ne|new|ng|nl|nn|no|nov|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|rw|sa|sah|sc|scn|sco|sd|se|sg|sgs|sh|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|zh-yue|za|zea|zu)\:(?!(wiktionary|wikt|wikinews|n|wikibooks|b|wikiquote|q|wikisource|s|oldwikisource|species|wikispecies|wikiversity|v|betawikiversity|wikimedia|foundation|wmf|wikivoyage|voy|commons|c|meta|metawikipedia|m|strategy|incubator|mediawikiwiki|mw|mediawiki|quality|otrswiki|otrs|ticket|phabricator|bugzilla|mediazilla|phab|nost|testwiki|wikidata|d|outreach|outreachwiki|toollabs|wikitech|dbdump|download|gerrit|mail|mailarchive|rev|spcom|sulutil|svn|tools|tswiki|wm2016|wm2017|wmania|User|Wikipedia|MediaWiki|Template|Help|File|Image|WP|Project|U|Special|利用者)\:)'
ilh='(?<!\{\{(Advtranslation|Plant\-translation|Translate|Translating|Translation[ _]+WIP|Translation|Trans|Tran|Voltranslation|Wptranslation|正在翻(譯|译)|(翻)?(譯|译)(中)?)[^\}]*)\[\[\:(aa|ab|ace|ady|af|ak|als|am|an|ang|ar|arc|arz|as|ast|av|ay|az|azb|ba|bar|bat-smg|bcl|be|be-tarask|be-x-old|bg|bh|bi|bjn|bm|bn|bo|bpy|br|bs|bug|bxr|ca|cbk-zam|cdo|ce|ceb|ch|cho|chr|chy|ckb|co|cr|crh|cs|csb|cu|cv|cy|da|de|diq|dsb|dv|dz|ee|egl|eml|el|en|eo|es|et|eu|ext|fa|ff|fi|fiu-vro|fj|fo|fr|frp|frr|fur|fy|ga|gag|gan|gd|gl|glk|gn|gom|got|gsw|als|gu|gv|ha|hak|haw|he|hi|hif|ho|hr|hsb|ht|hu|hy|hz|ia|id|ie|ig|ii|ik|ilo|io|is|it|iu|ja|jp|jam|jbo|jv|ka|kaa|kab|kbd|kg|ki|kj|kk|kl|km|kn|ko|koi|kr|krc|ks|ksh|ku|kv|kw|ky|la|lad|lb|lbe|lez|lg|li|lij|lmo|ln|lo|lrc|lt|ltg|lv|lzh|zh-classical|mai|map-bms|mdf|mg|mh|mhr|mi|min|mk|ml|mn|mo|mr|mrj|ms|mt|mus|mwl|my|myv|mzn|na|nah|nan|zh-min-nan|nap|nb|no|nds|nds-nl|ne|ne|new|ng|nl|nn|no|nov|nrm|nso|nv|ny|oc|olo|om|or|os|pa|pag|pam|pap|pcd|pdc|pfl|pi|pih|pl|pms|pnb|pnt|ps|pt|qu|rm|rmy|rn|ro|roa-rup|roa-tara|ru|rue|rup|rw|sa|sah|sc|scn|sco|sd|se|sg|sgs|sh|si|simple|sk|sl|sm|sn|so|sq|sr|srn|ss|st|stq|su|sv|sw|szl|ta|tcy|te|tet|tg|th|ti|tk|tl|tn|to|tpi|tr|ts|tt|tum|tw|ty|tyv|udm|ug|uk|ur|uz|ve|vec|vep|vi|vls|vo|vro|wa|war|wo|wuu|xal|xh|xmf|yi|yo|yue|zh-yue|za|zea|zu)\:(?!(wiktionary|wikt|wikinews|n|wikibooks|b|wikiquote|q|wikisource|s|oldwikisource|species|wikispecies|wikiversity|v|betawikiversity|wikimedia|foundation|wmf|wikivoyage|voy|commons|c|meta|metawikipedia|m|strategy|incubator|mediawikiwiki|mw|mediawiki|quality|otrswiki|otrs|ticket|phabricator|bugzilla|mediazilla|phab|nost|testwiki|wikidata|d|outreach|outreachwiki|toollabs|wikitech|dbdump|download|gerrit|mail|mailarchive|rev|spcom|sulutil|svn|tools|tswiki|wm2016|wm2017|wmania|User|Wikipedia|MediaWiki|Template|Help|File|Image|WP|Project|U|Special|利用者)\:)'

count=0

gen0 = site.search(ilh_search0,namespaces=0)
#ilh_search is too long for site.search and leads to "pywikibot.data.api.APIError: cirrussearch-query-too-long".

gen1 = pagegenerators.RegexBodyFilterPageGenerator(gen0, ilh_search, quantifier='any')
#ilh would cause "re.error: look-behind requires fixed-width pattern" because RegexBodyFilterPageGenerator uses "re" rather than "regex" package.

gen = pagegenerators.RegexBodyFilterPageGenerator(gen1, '\{\{Link style', quantifier='none')
#Skip pages with {{Link style}}.

for page in gen:
	count+=1
	art_txt = page.text
	ilh_list = re.findall(ilh,art_txt,re.I)
	print(count,page.title(),len(ilh_list))
	if(len(ilh_list)==0): continue
	page.text = '{{subst:Link style/auto}}\n' + art_txt
	page.save(u"機器人：標記不合[[WP:MOSIW|跨語言連結規範]]之頁面")

print('Done')