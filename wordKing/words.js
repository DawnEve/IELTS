/** 背单词序号和日期
目前mysql中一共8000多个单词，一天100个，需要80天过一遍。
前面的简单，一天多几点。
dict/scanWord.html?page=3&aim=5
日期 新背诵, 复习
2020.11.2 2-6;
2020.11.3 7,5-7;
2020.11.4 8-9,7;
2020.11.5 10, 8-9;
2020.11.6 11-12, 10;
2020.11.7 , 10;
2020.11.8 13-14, 11-12; 周日复习
2020.11.9 15, 14;
2020.11.10 16, 15;
2020.11.11 17, 15-16;



*/

var words=["escort", "antenna", "gallery", "conviction", "liberal", "imperial", "lawn", "voyage", "scrape", "spine",
"rectify", "anguish", "satire", "expire", "inherent", "salvation", "mute", "sprinkle",
"weave", "grip", "thrust", "paw", "gauge", "esteem", "anecdote", "chap", "rash", "bruise",
// page=3;
"ruthless", "uneasy", "retain", "wedge",
// page=4;
"monetary", "monotonous", "weld", "giggle", "analogue", "prudent", "defy", "inlet", "tribute",
// page=5;
"puppet", "articulate", "posture", "reproach", "discern", "trench", "jug", "gulf", "stationery", "discourse", "lapse", "celebrity", "exempt", "majesty", "adverse", "uphold", "sensation", "slim", "enclose", "escalate", "tug", 
//6
"magnet", "turnover", "pebble", "plight", "fringe", "aerial", "sneak", "squirrel", "premise", "deliberate",
"coherent", "incline", "proclaim",

//7
"scout", "dumb", "resolve", "oppress", "tan", "stab", "disposition", "lease", "plunge", "obstruct", "reckless", "manifest", "cradle", "prophet",
"prime", "outrage","detach",

//8
"graze", "marital", "hurl", "liberty", "eminent", "heritage", "derive", 
//9
"excerpt", "sane", "excess", "consent", "persevere", "outfit", 
//10
"bleak", "disperse", "superfluous", "brittle", "clash", "withstand", "abdomen", "dispose", "precedent", "reservoir",
//11
"revelation", "contend", "tramp", "customary", "prevalent", "heap", "lubricate",
//12
"distort", "desolate", "symmetry", "embody", "feminine", "perplex", "arithmetic", "advent", "temperament", "shove", "preach", "conceive", "tram", "sarcastic", "suspicion", "temperament", 
//13
"dew", "patron", "repertoire", "symposium", "panorama", "allege", "scramble", 
//14
"bullet", "doctorate", "lever", "constituent", "stalk", "perceive", "solitary", "intact", 
//15
"miniature", "spade", "glare", "brace", "advisable", "divine", "beloved", "resultant", "plumber", "abide", "orthodox", "hum", "scarf", "tempt", "gallop",
//16
"swamp", "compassion", "consensus", "pendulum", "verdict", "rally", "lofty", "indicative", 
//17
"prone", "diffuse", "snatch", "intermittent", "conspicuous", "diminish", 





"withhold", "lodge", "turbine", "vague", "spiral", "freight", "modest", "exquisite"]

