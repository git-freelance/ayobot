from whatsapp_bot.models import WhatsAppConversation
countries = [
  "afghanistan",
  "albania",
  "algeria",
  "angola",
  "argentina",
  "armenia",
  "aruba",
  "australia",
  "austria",
  "azerbaijan",
  "bahamas",
  "bahrain",
  "bangladesh",
  "barbados",
  "belarus",
  "belgium",
  "belize",
  "benin",
  "bhutan",
  "bolivia",
  "bosnia and herzegovina",
  "botswana",
  "brazil",
  "brunei darussalam",
  "bulgaria",
  "burkina faso",
  "burundi",
  "cambodia",
  "cameroon",
  "canada",
  "cape verde",
  "central african republic",
  "chad",
  "channel islands",
  "chile",
  "china",
  "china, hong kong special administrative region",
  "china, macao special administrative region",
  "colombia",
  "comoros",
  "congo",
  "costa rica",
  "côte d'ivoire",
  "croatia",
  "cuba",
  "cyprus",
  "czech republic",
  "democratic people's republic of korea",
  "democratic republic of the congo",
  "denmark",
  "djibouti",
  "dominican republic",
  "ecuador",
  "egypt",
  "el Salvador",
  "equatorial Guinea",
  "eritrea",
  "estonia",
  "ethiopia",
  "fiji",
  "finland",
  "france",
  "french guiana",
  "french polynesia",
  "gabon",
  "gambia",
  "georgia",
  "germany",
  "ghana",
  "greece",
  "grenada",
  "guadeloupe",
  "guam",
  "guatemala",
  "guinea",
  "guinea-bissau",
  "guyana",
  "haiti",
  "honduras",
  "hungary",
  "iceland",
  "india",
  "indonesia",
  "iran",
  "iraq",
  "ireland",
  "israel",
  "italy",
  "jamaica",
  "japan",
  "jordan",
  "kazakhstan",
  "kenya",
  "kuwait",
  "kyrgyzstan",
  "lao",
  "latvia",
  "lebanon",
  "lesotho",
  "liberia",
  "libya",
  "lithuania",
  "luxembourg",
  "madagascar",
  "malawi",
  "malaysia",
  "maldives",
  "mali",
  "malta",
  "martinique",
  "mauritania",
  "mauritius",
  "mayotte",
  "mexico",
  "micronesia",
  "mongolia",
  "montenegro",
  "morocco",
  "mozambique",
  "myanmar",
  "namibia",
  "nepal",
  "netherlands",
  "netherlands antilles",
  "new caledonia",
  "new zealand",
  "nicaragua",
  "niger",
  "nigeria",
  "norway",
  "occupied palestinian territory",
  "oman",
  "pakistan",
  "panama",
  "papua new guinea",
  "paraguay",
  "peru",
  "philippines",
  "poland",
  "portugal",
  "puerto rico",
  "qatar",
  "republic of korea",
  "republic of moldova",
  "réunion",
  "romania",
  "russian federation",
  "rwanda",
  "saint lucia",
  "saint vincent and the grenadines",
  "samoa",
  "sao tome and principe",
  "saudi arabia",
  "senegal",
  "serbia",
  "sierra leone",
  "singapore",
  "slovakia",
  "slovenia",
  "solomon islands",
  "somalia",
  "south africa",
  "spain",
  "sri lanka",
  "sudan a",
  "suriname",
  "swaziland",
  "sweden",
  "switzerland",
  "syrian arab republic",
  "tajikistan",
  "tanzania",
  "thailand",
  "macedonia",
  "timor-leste",
  "togo",
  "tonga",
  "trinidad and tobago",
  "tunisia",
  "turkey",
  "turkmenistan",
  "uganda",
  "ukraine",
  "united arab emirates",
  "united kingdom",
  "united states of america",
  "uruguay",
  "uzbekistan",
  "vanuatu",
  "venezuela",
  "viet nam",
  "virgin islands",
  "western sahara",
  "yemen",
  "zambia",
  "zimbabwe",
];

nations = [
  "afghan albanian",
  "algerian",
  "american",
  "andorran",
  "angolan",
  "anguillan",
  "citizen of antigua and barbuda",
  "argentine",
  "armenian",
  "australian",
  "austrian",
  "azerbaijani",
  "bahamian",
  "bahraini",
  "bangladeshi",
  "barbadian",
  "belarusian",
  "belgian",
  "belizean",
  "beninese",
  "bermudian",
  "bhutanese",
  "bolivian",
  "citizen of bosnia and herzegovina",
  "botswanan",
  "brazilian",
  "british",
  "british virgin islander",
  "bruneian",
  "bulgarian",
  "burkinan",
  "burmese",
  "burundian",
  "cambodian",
  "cameroonian",
  "canadian",
  "cape verdean",
  "cayman islander",
  "central african",
  "chadian",
  "chilean",
  "chinese",
  "colombian",
  "comoran",
  "congolese (congo)",
  "congolese (drc)",
  "cook islander",
  "costa rican",
  "croatian",
  "cuban",
  "cymraes",
  "cymro",
  "cypriot",
  "czech",
  "danish",
  "djiboutian",
  "dominican",
  "citizen of the dominican republic",
  "dutch",
  "east timorese",
  "ecuadorean",
  "egyptian",
  "emirati",
  "british",
  "equatorial guinean",
  "eritrean",
  "estonian",
  "ethiopian",
  "faroese",
  "fijian",
  "filipino finnish",
  "french",
  "gabonese",
  "gambian",
  "georgian",
  "german",
  "ghanaian",
  "gibraltarian",
  "greek",
  "greenlandic",
  "grenadian",
  "guamanian",
  "guatemalan",
  "citizen of guinea-bissau",
  "guinean",
  "guyanese",
  "haitian",
  "honduran",
  "hong konger",
  "hungarian",
  "icelandic",
  "indian",
  "indonesian",
  "iranian",
  "iraqi",
  "irish",
  "israeli",
  "italian",
  "ivorian",
  "jamaican",
  "japanese",
  "jordanian",
  "kazakh",
  "kenyan",
  "kittitian",
  "citizen of kiribati",
  "kosovan",
  "kuwaiti",
  "kyrgyz",
  "lao",
  "latvian",
  "lebanese",
  "liberian",
  "libyan",
  "liechtenstein citizen",
  "lithuanian",
  "luxembourger",
  "macanese",
  "macedonian",
  "malagasy",
  "malawian",
  "malaysian",
  "maldivian",
  "malian",
  "maltese",
  "marshallese",
  "martiniquais",
  "mauritanian",
  "mauritian",
  "mexican",
  "micronesian",
  "moldovan",
  "monegasque",
  "mongolian",
  "montenegrin",
  "montserratian",
  "moroccan",
  "mosotho",
  "mozambican",
  "namibian",
  "nauruan",
  "nepalese",
  "new zealander",
  "nicaraguan",
  "nigerian",
  "nigerien",
  "niuean",
  "north korean",
  "northern irish",
  "norwegian",
  "omani",
  "pakistani",
  "palauan",
  "palestinian",
  "panamanian",
  "papua new guinean",
  "paraguayan",
  "peruvian",
  "pitcairn islander",
  "polish",
  "portuguese",
  "prydeinig",
  "puerto rican",
  "qatari",
  "romanian",
  "russian",
  "rwandan",
  "salvadorean",
  "sammarinese",
  "samoan",
  "sao tomean",
  "saudi arabian",
  "scottish",
  "senegalese",
  "serbian",
  "citizen of seychelles",
  "sierra leonean",
  "singaporean",
  "slovak",
  "slovenian",
  "solomon islander",
  "somali south african",
  "south korean",
  "south sudanese",
  "spanish",
  "sri lankan",
  "st helenian",
  "st lucian",
  "stateless",
  "sudanese",
  "surinamese",
  "swazi",
  "swedish",
  "swiss",
  "syrian",
  "taiwanese",
  "tajik",
  "tanzanian",
  "thai",
  "togolese",
  "tongan",
  "trinidadian",
  "tristanian",
  "tunisian",
  "turkish turkmen",
  "turks and caicos islander",
  "tuvaluan",
  "ugandan",
  "ukrainian",
  "uruguayan",
  "uzbek",
  "vatican citizen citizen of vanuatu",
  "venezuelan",
  "vietnamese",
  "vincentian",
  "wallisian",
  "welsh",
  "yemeni",
  "zambian",
  "zimbabwean",
]


def get_message_by_content_sid(wa_id, content_sid):
    """Retrieve the last message for a specific WhatsApp ID and content SID."""
    conversation = WhatsAppConversation.objects.filter(
        wa_id=wa_id,
        content_sid=content_sid
    ).order_by('-created_at').first()
    return conversation.message if conversation else None

def split_message(text, chunk_size=1600):
    """Split a message into chunks of specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
