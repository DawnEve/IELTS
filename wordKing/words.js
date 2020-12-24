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
2020.11.12 18, _;
2020.11.13 19, 16-18;
2020.11.14 20, 19; 
2020.11.15 21, 20; 周日复习

2020.11.16 22, 21; 

2020.11.18 23, 22;
 
2020.11.20 24, 23; 
2020.11.21 25, ; 
2020.11.22 26, 25; 
2020.11.23 27, 26; 

2020.11.25 28, 26-27; 
2020.11.26 29, ; 
2020.11.27 30, 28-29; 

2020.11.30 31, ; 

2020.12.2 32, 30-31; 

2020.12.4 33, 31-32; 

2020.12.6 34, 32-33; 
2020.12.7 35, ; 
2020.12.10 36-38, 34-35; 
2020.12.11 39, 37-38; 
2020.12.13 40-41, 39; 周日复习

2020.12.15 42-43, 40-41;
2020.12.16 44, 43;
2020.12.17 45-46, 44;
2020.12.18 47, 46;
2020.12.19 48-50, 46-47;

2020.12.21 51, 49-50;
2020.12.22 52-53, 50-51;
2020.12.23 54, ;



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
"scrutiny", "restraint", "foul", "orient", 

//18
"whirl", "swarm", "constitute", "textile", "stake", "instantaneous", "clutch", "intrude", "overtake", "plausible", "linen", 
//19
"deem", "sovereign", "assault", "sham", "prompt", "kin", "integrity", "siege", "bolt", "staple", "descendant", "inferior", "lumber", 
//20
"aural", "rip", "retrospect", "fertile", "priest", "stun", "militant", 
"intricate", "immerse", 
//21
"meditate", "circumference", "crust", "paradigm", "eternal", "stumble", "canal", "incur", "municipal", "stool", "rein", "desperate", "fable", "affection", "hypocrisy", "apt", "invariably", 
//22
"homogeneous", "epoch", "fume", "overpass", "trolley", "grope", "cordial", "astronaut", "deteriorate", "poultry", "canoe", 

//23
"flush", "cosy", "scrap", "discreet", "autonomy", "shed", "radiant", "mourn", 
//24
"relevant", "vacuum", "reel", "flock", "solidarity", "cart", "grieve", "revolve", 
//25
"sniff", "plead", "deficit", "exert", "wreck", "mock", "clap", "favorable", "jaw", "fountain", "metric", "distress", "conspiracy", 
//26
"extravagant", "erroneous", "implication", "slack", 
"formulate", "liberate", 
//27
"petty", "pretext", "indulge", "drastic", "jargon", "impetus", "formidable", "niece", "mercury", "blunder", "slit", "obstruction", 

//28
"contrive", "appal", "dine", "turbine", "transcend", "feudal", "slum", "exquisite", "overhead", "withhold", 
"lodge", "vague", "spiral", "freight", "modest", 
//29
"disgrace", "stern", "flap", "barn", "racket", "skull", "ashore", "outlet", "knob", "splash", "huddle", "exaggerate", "liquor", 

//30
"reciprocal", "elastic", "shady", "vowel", "caress", "faculty", "compulsory", 

//31
"eccentric", "stoop", "captive", "dividend", "bowl", "contempt", "crane", "agony", "ample", "cardinal",
//32
"muscular", "tow", "inhale", "abound", "psychiatry", "aspire", "spectator", "colonel", "biscuit", 
//33
"trivial", "vulgar", "statute", "concede", "remnant", "despise", "ebb", "grim", "bore", "orchestra", "arrogant", "recede", "Catholic", "intrigue", "divert", "clergy", "obedience", 
"friction", 

//compose 组成，构成
//34
"envisage", "biography", "emigrate", "stall", "verbal", "veil", "tub", "creep", "veteran", "endow", 
"torment", 
//35
"mob", "fragrant", "bow", "addict", "prestige", "linguistic", "wrench", "maneuver", "clasp", "excessive", "gown",
"enclosure", "transient", 
//36
"indignant", "trifle", "wink", 
//37
"susceptible", "liable", "premium", "noble", "descent", "contract",
"expend", "inverse", "cohesive", "refuge",
//38
"rigid", "breach", "orchard", "conscientious", "intimate", "interim", "moss", "hospitality", "savage", "contrast", "strife", "commodity",
"mischief", "ascertain", "integral", 
//39
"hinge", "plaster", "avert", "aggravate", "persecute", "illiterate", "steward", "verge", "hostile", "tumble",
"utmost", "reckon",
//40
"wrinkle", "monopoly", "treason", "beverage", "obscure", "spin", "jolly", "librarian", "detain", "tuck", "irritate", "discrepancy", "comrade", "cafeteria",
//41
"notwithstanding", "howl", "plateau", "propel", "cunning", "provision", "riddle",
"contemplate", "exotic",
//42
"scorn", "synthesis", "oriental", "composite", "entail", "diversion", "elaborate",
//43
"grind", "juvenile", "gum", "slender", "confess", "fracture", "scratch", "pedestrian", "preliminary", "hoist", "outset",
"progressive", "piston",
//44
"outward", "fraud", "amiable", "moderate", "mortgage", "scold", "expedition",
//45
"malignant", "preferable", "wreath", "alloy",
//46
"hysterical", "revolt", "proposition", "convict", "perpetual",
"refute", "denounce", "renovate",
"sentiment", "edible", "screw", "rap", "insult",
//47
"pirate", "wholesome", "mould", "lounge", "concession", "tribe", "pitch", "fabulous", "sew", "dissipate", "genius", "retort", 
"fabric", 
//48
"legitimate", "tiresome", "credential", "crawl", "relish", "grab", "seam", "cricket", "humid", "expenditure", "feasible",
//49
"recur", "imperative", "sly", "agitate",
"pathetic", "permeate", 
//50
"precede", "cape", "corrode", "foster", "consecutive", "gracious", "uproar", "preclude", "shaft", "soak", "irony", "sprout", 
"applicable", "drain",  
//51
"gratitude", "preside", "orientation", "bracket", "bibliography", "setback", "squeeze", "analytic", "unanimous", "magnitude", "stale",
"groan", "dread", 
//52
"assassinate", "subordinate", "stroll", "prose", "humidity", "speciality", "stationary", "artery", "hut", "memorial", "verse", "exploit",
//53
"ballot", "futile", "wretched", "hop", "obsolete", "numb", "thrift", "lest", "deprive", "likewise", "stitch", 
//54
"stubborn", "shrewd", "nucleus", "cognitive", "booth", "cord", "brim", "ingenious", 

]
