import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ============================================================
# HARDCODED TOKENIZER DATA (from uploaded tokenizer_report.json)
# ============================================================

tokenizer_report = {
    "prompt_length_chars": 4644,
    "deepseek": {
        "total_tokens": 1120,
        "tokens": [
            "{", "\n", "", "\"", "role", "\":", "\"", "Senior", "Business", "Process",
            "Management", "(", "B", "PM", ")", "Analyst", "\",", "\n", "", "\"",
            "special", "ization", "\":", "\"", "Health", "care", "administration",
            "and", "patient", "flow", "optimization", "\",", "\n", "", "\"",
            "experience", "\":", "\"", "1", "5", "+", "years", "\",", "\n", "",
            "\"", "context", "\":", "\"", "You", "are", "decom", "posing", "a",
            "standard", "in", "-", "person", "patient", "registration", "process",
            "at", "a", "hospital", "front", "desk", "to", "create", "a", "step",
            "-", "by", "-", "step", "Standard", "Operating", "Procedure", "(",
            "S", "OP", ")", ".", "The", "staff", "member", "has", "access", "to",
            "a", "Hospital", "Information", "System", "(", "H", "IS", ")", ",",
            "a", "document", "scanner", ",", "and", "a", "printer", ".", "Your",
            "output", "will", "be", "used", "as", "a", "training", "checklist",
            "for", "new", "front", "-", "desk", "registration", "staff", ".\"",
            ",", "\n", "", "\"", "task", "\":", "\"", "De", "compose", "each",
            "high", "-", "level", "activity", "from", "the", "provided", "list",
            "into", "a", "sequence", "of", "granular", ",", "executable", "subst",
            "eps", "that", "a", "staff", "member", "can", "follow", "without",
            "guess", "work", ".\"", ",", "\n", "", "\"", "input", "\":", "{",
            "\n", "  ", "\"", "process", "_", "name", "\":", "\"", "Patient",
            "Registers", "in", "the", "hospital", "\",", "\n", "  ", "\"",
            "activities", "\":", "[", "\n", "    ", "{", "\n", "      ",
            "\"", "activity", "_", "id", "\":", "\"", "A", "1", "\",", "\n",
            "      ", "\"", "activity", "_", "name", "\":", "\"", "Record",
            "the", "data", "of", "each", "patient", "\",", "\n", "      ",
            "\"", "description", "\":", "\"", "Create", "initial", "patient",
            "record", "in", "the", "hospital", "information", "system", "and",
            "collect", "basic", "demographic", "information", "\"", "\n",
            "    ", "}", ",", "\n", "    ", "{", "\n", "      ", "\"",
            "activity", "_", "id", "\":", "\"", "A", "2", "\",", "\n",
            "      ", "\"", "activity", "_", "name", "\":", "\"", "Register",
            "the", "SS", "N", "of", "the", "patient", "\",", "\n", "      ",
            "\"", "description", "\":", "\"", "Capture", "and", "validate",
            "patient", "'", "s", "Social", "Security", "Number", "for",
            "insurance", "and", "identification", "\"", "\n", "    ", "}",
            ",", "\n", "    ", "{", "\n", "      ", "\"", "activity", "_", "id",
            "\":", "\"", "A", "3", "\",", "\n", "      ", "\"", "activity",
            "_", "name", "\":", "\"", "Register", "the", "Name", "of", "the",
            "patient", "\",", "\n", "      ", "\"", "description", "\":",
            "\"", "Record", "patient", "'", "s", "legal", "first", "and",
            "middle", "name", "(", "s", ")", "from", "official", "ID", "\"",
            "\n", "    ", "}", ",", "\n", "    ", "{", "\n", "      ", "\"",
            "activity", "_", "id", "\":", "\"", "A", "4", "\",", "\n",
            "      ", "\"", "activity", "_", "name", "\":", "\"", "Register",
            "the", "S", "urname", "of", "the", "patient", "\",", "\n",
            "      ", "\"", "description", "\":", "\"", "Record", "patient",
            "'", "s", "family", "name", "for", "records", "and", "billing",
            "\"", "\n", "    ", "}", ",", "\n", "    ", "{", "\n", "      ",
            "\"", "activity", "_", "id", "\":", "\"", "A", "5", "\",", "\n",
            "      ", "\"", "activity", "_", "name", "\":", "\"", "Print",
            "referral", "document", "\",", "\n", "      ", "\"", "description",
            "\":", "\"", "Generate", "and", "print", "official", "registration",
            "confirmation", "for", "consultation", "\"", "\n", "    ", "}",
            ",", "\n", "    ", "{", "\n", "      ", "\"", "activity", "_", "id",
            "\":", "\"", "A", "6", "\",", "\n", "      ", "\"", "activity",
            "_", "name", "\":", "\"", "Archive", "the", "record", "in", "file",
            "system", "\",", "\n", "      ", "\"", "description", "\":",
            "\"", "Store", "completed", "registration", "record", "securely",
            "for", "compliance", "and", "retrieval", "\"", "\n", "    ", "}",
            "\n", "  ", "]", "\n", "", "}", "\n", "", "\"", "output",
            "_", "format", "\":", "{", "\n", "  ", "\"", "structure",
            "\":", "\"", "Return", "a", "valid", "JSON", "object", "with",
            "a", "single", "key", "\\\"", "decomposition", "_", "result",
            "\\\"", "containing", "an", "array", "of", "decomposed",
            "activities", ".\"", ",", "\n", "  ", "\"", "schema", "\":",
            "{", "\n", "    ", "\"", "decomposition", "_", "result",
            "\":", "[", "\n", "      ", "{", "\n", "        ", "\"",
            "activity", "_", "id", "\":", "\"", "String", ".", "Must",
            "exactly", "match", "the", "input", ".\"", ",", "\n", "        ",
            "\"", "activity", "_", "name", "\":", "\"", "String", ".",
            "MUST", "EX", "ACT", "LY", "MATCH", "the", "'", "activity",
            "_", "name", "'", "from", "input", ",", "character", "-",
            "for", "-", "character", ",", "including", "spaces", "and",
            "punctuation", ".", "Do", "not", "paraphrase", ",", "re",
            "word", ",", "or", "modify", ".\"", ",", "\n", "        ",
            "\"", "sub", "steps", "\":", "[", "\n", "          ", "{",
            "\n", "            ", "\"", "step", "_", "number", "\":",
            "\"", "Integer", ".", "Sequ", "ential", "starting", "from",
            "", "1", ".\"", ",", "\n", "            ", "\"", "description",
            "\":", "\"", "String", ".", "Single", "atomic", "instruction",
            "starting", "with", "an", "imperative", "verb", ".\"", "\n",
            "          ", "}", "\n", "        ", "]", "\n", "      ",
            "}", "\n", "    ", "]", "\n", "  ", "}", "\n", "", "}",
            ",", "\n", "", "\"", "few", "_", "shot", "_", "learning", "\":",
            "{", "\n", "  ", "\"", "activity", "_", "name", "\":",
            "\"", "Store", "and", "print", "notice", "\",", "\n", "  ",
            "\"", "sub", "steps", "\":", "[", "\n", "    ", "{", "\n",
            "      ", "\"", "step", "_", "number", "\":", "", "1", ",",
            "\n", "      ", "\"", "description", "\":", "\"", "Save",
            "notice", "in", "digital", "system", "\"", "\n", "    ",
            "}", ",", "\n", "    ", "{", "\n", "      ", "\"", "step",
            "_", "number", "\":", "", "2", ",", "\n", "      ", "\"",
            "description", "\":", "\"", "Print", "physical", "copy", "of",
            "notice", "\"", "\n", "    ", "}", ",", "\n", "    ", "{",
            "\n", "      ", "\"", "step", "_", "number", "\":", "", "3",
            ",", "\n", "      ", "\"", "description", "\":", "\"", "File",
            "printed", "notice", "\"", "\n", "    ", "}", "\n", "  ",
            "]", "\n", "", "}", ",", "\n", "", "\"", "decomposition",
            "_", "rules", "\":", "{", "\n", "  ", "\"", "gran",
            "ularity", "_", "rule", "\":", "\"", "A", "im", "for", "",
            "3", "to", "", "5", "subst", "eps", "per", "activity", ".",
            "Keep", "it", "minimal", "if", "the", "description", "is",
            "simple", ".\"", ",", "\n", "  ", "\"", "atomic", "ity",
            "_", "rule", "\":", "\"", "Each", "subst", "ep", "must", "be",
            "one", "observable", "staff", "action", "with", "one", "clear",
            "outcome", ".\"", ",", "\n", "  ", "\"", "hierarchy",
            "_", "rule", "\":", "\"", "Treat", "each", "input", "activity",
            "as", "independent", ".", "Do", "not", "merge", "steps",
            "across", "activities", ".\"", ",", "\n", "  ", "\"",
            "content", "_", "constraints", "\":", "[", "\n", "    ",
            "\"", "Describe", "ONLY", "observable", "staff", "actions",
            "and", "direct", "interactions", ".\"", ",", "\n", "    ",
            "\"", "Do", "NOT", "describe", "internal", "system",
            "processes", "or", "background", "checks", ".\"", ",", "\n",
            "    ", "\"", "Do", "NOT", "include", "clinical", "judgment",
            "or", "medical", "advice", ".\"", ",", "\n", "    ", "\"",
            "Base", "decomposition", "STRICT", "LY", "on", "the", "'",
            "description", "'", "field", ".", "Do", "not", "infer",
            "extra", "steps", ".\"", "\n", "  ", "]", ",", "\n", "  ",
            "\"", "quality", "_", "criteria", "\":", "[", "\n", "    ",
            "\"", "Logical", "Flow", ":", "Correct", "practical", "order",
            ".\"", ",", "\n", "    ", "\"", "Cl", "arity", "&",
            "Action", "ability", ":", "Un", "ambiguous", "direct",
            "commands", ".\"", ",", "\n", "    ", "\"", "Comple",
            "teness", ":", "Fully", "acco", "mplishe", "s", "the",
            "activity", "goal", ".\"", ",", "\n", "    ", "\"",
            "Format", "Compliance", ":", "Every", "description",
            "starts", "with", "an", "imperative", "verb", ".\"", ",",
            "\n", "    ", "\"", "Name", "Integrity", ":", "activity",
            "_", "name", "MUST", "be", "copied", "verb", "atim",
            "from", "input", "", "-", "no", "modifications", "allowed",
            ".\"", "\n", "  ", "]", "\n", "", "}", ",", "\n", "",
            "\"", "final", "_", "instruction", "\":", "\"", "Process",
            "'", "input", ".", "activities", "'", ".", "Apply", "all",
            "rules", ".", "Output", "ONLY", "a", "single", "JSON",
            "object", "with", "the", "key", "\\\"", "decomposition",
            "_", "result", "\\\"", "containing", "the", "array", ".",
            "CR", "ITICAL", ":", "Every", "activity", "_", "name",
            "in", "your", "output", "must", "match", "the", "input",
            "activity", "_", "name", "EX", "ACT", "LY", ",", "character",
            "-", "for", "-", "character", ".", "No", "markdown", ",",
            "no", "extra", "text", ",", "no", "explanations", ".",
            "Use", "the", "example", "in", "'", "few", "_", "shot",
            "_", "learning", "'", "as", "a", "template", "for", "the",
            "structure", "and", "granularity", "of", "subst", "eps",
            ".\"", "\n", "}"
        ]
    },
    "gemini": {
        "total_tokens": 1109,
        "tokens": [
            "{", "\n", " ", " \"", "r", "ole\"", ": ", "\"S",
            "eni", "or Busi", "ness Proce", "ss Manag", "eme", "nt (BPM",
            ")", " ", "Analys", "t\",\n", " ", " \"", "s", "peci",
            "alizati", "on\": ", "\"H", "ea", "lthcare admini", "stration and ",
            "patie", "nt flow ", "opti", "mizati", "on\",\n ", " \"",
            "e", "xpe", "rienc", "e\": \"1", "5", "+", " ", "years\"",
            ",\n", " ", " \"", "c", "ontex", "t\": ", "\"Y",
            "ou ", "are ", "decompo", "si", "ng a standa", "rd in-",
            "p", "erso", "n patie", "nt regis", "tration proce", "ss at ",
            "a ", "hospi", "tal front ", "desk ", "to ", "create ",
            "a ", "step-", "b", "y-", "s", "tep ", "Standa",
            "rd Ope", "rating Proce", "dure (S", "OP", ")", ". ",
            "The ", "staff ", "membe", "r has ", "acce", "ss to ",
            "a ", "Hospi", "tal Infor", "mation Syste", "m (H", "IS)",
            ", ", "a ", "docu", "ment sca", "nner, ", "and ", "a ",
            "printe", "r. ", "Your ", "outpu", "t will ", "be ",
            "used ", "as ", "a ", "traini", "ng chec", "klist for ",
            "new ", "front-", "d", "esk ", "regis", "tration staff.",
            "\",\n", " ", " \"", "t", "ask\"", ": ", "\"D",
            "eco", "mpo", "se eac", "h high-", "l", "evel ", "acti",
            "vity from ", "the ", "provi", "ded list ", "into ", "a ",
            "seque", "nce of ", "granu", "lar, ", "execu", "table subste",
            "ps ", "that ", "a ", "staff ", "membe", "r can ", "follo",
            "w witho", "ut gues", "swork.\",\n", " ", " \"",
            "i", "npu", "t\": ", "{\n", " ", "   \"",
            "p", "roce", "ss_n", "ame\"", ": ", "\"P",
            "ati", "ent Regi", "sters in ", "the ", "hospi", "tal\",\n",
            " ", "   \"", "a", "ctivi", "ties\": ", "[\n",
            " ", "     {", "\n", " ", "       \"",
            "a", "ctivi", "ty_i", "d\"", ": ", "\"A",
            "1", "\"", ",\n", " ", "       \"",
            "a", "ctivi", "ty_n", "ame\"", ": ", "\"R",
            "ecor", "d the ", "data ", "of ", "eac", "h patie",
            "nt\",\n", " ", "       \"", "d", "escri",
            "pti", "on\": \"C", "rea", "te initia", "l patie", "nt record ",
            "in ", "the ", "hospi", "tal infor", "mation syste", "m and ",
            "collec", "t basic ", "demog", "raphi", "c information\"\n",
            " ", "     }", ",\n", " ", "     {", "\n",
            " ", "       \"", "a", "ctivi", "ty_i", "d\"",
            ": ", "\"A", "2", "\"", ",\n", " ", "       \"",
            "a", "ctivi", "ty_n", "ame\"", ": ", "\"R",
            "egi", "ster the ", "SSN", " ", "of ", "the ", "patie",
            "nt\",\n", " ", "       \"", "d", "escri",
            "pti", "on\": \"C", "aptu", "re and ", "validat",
            "e patie", "nt's", " ", "Socia", "l Secu", "rity Numb",
            "er for ", "insu", "rance and ", "iden", "tification\"\n",
            " ", "     }", ",\n", " ", "     {", "\n",
            " ", "       \"", "a", "ctivi", "ty_i", "d\"",
            ": ", "\"A", "3", "\"", ",\n", " ", "       \"",
            "a", "ctivi", "ty_n", "ame\"", ": ", "\"R",
            "egi", "ster the ", "Name ", "of ", "the ", "patie",
            "nt\",\n", " ", "       \"", "d", "escri",
            "pti", "on\": \"R", "ecor", "d patie", "nt's", " ",
            "legal ", "firs", "t and ", "middl", "e name(", "s",
            ")", " ", "from ", "offi", "cial ID\"", "\n",
            " ", "     }", ",\n", " ", "     {", "\n",
            " ", "       \"", "a", "ctivi", "ty_i", "d\"",
            ": ", "\"A", "4", "\"", ",\n", " ", "       \"",
            "a", "ctivi", "ty_n", "ame\"", ": ", "\"R",
            "egi", "ster the ", "Surn", "am", "e of the ", "patie",
            "nt\",\n", " ", "       \"", "d", "escri",
            "pti", "on\": \"R", "ecor", "d patie", "nt's", " ",
            "fami", "ly name ", "for ", "records ", "and ", "billin",
            "g\"\n", " ", "     }", ",\n", " ", "     {", "\n",
            " ", "       \"", "a", "ctivi", "ty_i", "d\"",
            ": ", "\"A", "5", "\"", ",\n", " ", "       \"",
            "a", "ctivi", "ty_n", "ame\"", ": ", "\"P",
            "rint ", "referr", "al docu", "ment\",\n", " ", "       \"",
            "d", "escri", "pti", "on\": \"G", "enera", "te and ",
            "print ", "offi", "cial regis", "tration confirmat", "io",
            "n for consu", "ltation\"\n", " ", "     }", ",\n",
            " ", "     {", "\n", " ", "       \"",
            "a", "ctivi", "ty_i", "d\"", ": ", "\"A",
            "6", "\"", ",\n", " ", "       \"", "a",
            "ctivi", "ty_n", "ame\"", ": ", "\"A",
            "rchi", "ve the ", "record ", "in ", "file ", "syste",
            "m\",\n", " ", "       \"", "d", "escri",
            "pti", "on\": \"S", "tore ", "completed ", "regis",
            "tration record ", "securel", "y for ", "compli",
            "anc", "e and retri", "eva", "l\"\n ", "     }",
            "\n", " ", "   ]", "\n", " ", " }",
            ",\n", " ", " \"", "o", "utp", "ut_f", "ormat\"",
            ": ", "{\n", " ", "   \"", "s", "truc",
            "ture\": ", "\"R", "etu", "rn a ", "valid ", "JSO",
            "N objec", "t with ", "a ", "singl", "e key ",
            "\\\"d", "ecom", "po", "sitio", "n_result\\\" ", "contai",
            "ning an ", "array ", "of ", "decompo", "sed acti",
            "vities.\",\n", " ", "   \"", "s", "chem",
            "a\": ", "{\n", " ", "     \"", "d",
            "ecom", "po", "sitio", "n_result\": ", "[\n",
            " ", "       {", "\n", " ", "         \"",
            "a", "ctivi", "ty_i", "d\"", ": ", "\"S",
            "trin", "g. ", "Must ", "exa", "ctly matc", "h the ",
            "inpu", "t.\",\n", " ", "         \"", "a",
            "ctivi", "ty_n", "ame\"", ": ", "\"S",
            "trin", "g. ", "MUST ", "EXA", "CTLY ", "MATC",
            "H the ", "'a", "ctivi", "ty_n", "ame'",
            " ", "from ", "inpu", "t, ", "chara", "cter-f",
            "or-", "c", "hara", "cter, ", "includi", "ng spaces ",
            "and ", "punc", "tuation. ", "Do ", "not ", "paraph",
            "ra", "se, rewo", "rd,", " ", "or ", "modif",
            "y.\",\n", " ", "         \"", "s",
            "ubst", "eps\"", ": ", "[\n", " ", "           {",
            "\n", " ", "             \"", "s",
            "tep_", "n", "umb", "er\": ", "\"I",
            "nteg", "er. ", "Seque", "ntia", "l starting from ",
            "1", ".", "\",\n", " ", "             \"", "d",
            "escri", "pti", "on\": \"S", "trin",
            "g. ", "Singl", "e atomi", "c instruc", "tion starti",
            "ng with ", "an ", "impera", "tive verb.",
            "\"\n", " ", "           }", "\n", " ", "         ]",
            "\n", " ", "       }", "\n", " ", "     ]",
            "\n", " ", "   }", "\n", " ", " }",
            ",\n", " ", " \"", "f", "ew_", "s",
            "hot_", "l", "earni", "ng\": ", "{\n",
            " ", "   \"", "a", "ctivi", "ty_n", "ame\"",
            ": ", "\"S", "tore ", "and ", "print ", "noti",
            "ce\",\n", " ", "   \"", "s", "ubst",
            "eps\"", ": ", "[\n", " ", "     {", "\n",
            " ", "       \"", "s", "tep_", "n",
            "umb", "er\": ", "1", ",", "\n", " ", "       \"",
            "d", "escri", "pti", "on\": \"S", "ave ",
            "noti", "ce in ", "digi", "tal syste", "m\"\n",
            " ", "     }", ",\n", " ", "     {", "\n",
            " ", "       \"", "s", "tep_", "n",
            "umb", "er\": ", "2", ",", "\n", " ", "       \"",
            "d", "escri", "pti", "on\": \"P", "rint ",
            "physica", "l copy ", "of ", "noti", "ce\"\n",
            " ", "     }", ",\n", " ", "     {", "\n",
            " ", "       \"", "s", "tep_", "n",
            "umb", "er\": ", "3", ",", "\n", " ", "       \"",
            "d", "escri", "pti", "on\": \"F", "ile ",
            "printe", "d noti", "ce\"\n", " ", "     }",
            "\n", " ", "   ]", "\n", " ", " }",
            ",\n", " ", " \"", "d", "ecom",
            "po", "sitio", "n_rules\": ", "{\n", " ", "   \"",
            "g", "ranu", "lari", "ty_r", "ule\"", ": ", "\"A",
            "im ", "for ", "3", " ", "to ", "5", " ",
            "subste", "ps ", "per ", "acti", "vity. ", "Keep ",
            "it ", "minimal ", "if ", "the ", "descr", "iption is ",
            "simple.", "\"", ",\n", " ", "   \"", "a",
            "tomi", "city_", "r", "ule\"", ": ", "\"E",
            "a", "ch subste", "p ", "must ", "be ", "one ", "obse",
            "rvable staff ", "acti", "on with ", "one ", "clea",
            "r outc", "ome.\"", ",\n", " ", "   \"",
            "h", "ie", "rarchy_r", "ule\"", ": ", "\"T",
            "rea", "t eac", "h inpu", "t acti", "vity as ", "indep",
            "endent. ", "Do ", "not ", "merg", "e steps ", "acr",
            "oss acti", "vities.\"", ",\n", " ", "   \"",
            "c", "ontent_", "c", "onstra", "ints\": ", "[\n",
            " ", "     \"", "D", "escr",
            "ibe ONL", "Y obse", "rvable staff ", "acti",
            "ons and ", "direct ", "intera", "ctions.\"", ",\n",
            " ", "     \"", "D", "o ", "NOT ", "descr",
            "ibe internal ", "syste", "m proce", "sses or ", "backg",
            "roun", "d checks.\"", ",\n", " ", "     \"",
            "D", "o ", "NOT ", "include ", "clini",
            "cal judgm", "ent or ", "medical ", "advi", "ce.\"", ",\n",
            " ", "     \"", "B", "ase ", "decompo",
            "si", "tion STRICTLY ", "on ", "the ", "'d",
            "escri", "pti", "on' field.", " ", "Do ", "not ",
            "infer ", "extra ", "steps.", "\"", "\n", " ", "   ]",
            ",\n", " ", "   \"", "q", "ualit",
            "y_c", "rite", "ri", "a\": [\n", " ", "     \"",
            "L", "ogi", "cal Flow:", " ", "Correc", "t practi",
            "cal order.", "\"", ",\n", " ", "     \"", "C",
            "lari", "ty ", "& ", "Acti", "onability:", " ", "Unam",
            "big", "uou", "s direct ", "comman", "ds.\"", ",\n",
            " ", "     \"", "C", "omplet",
            "enes", "s: ", "Fully ", "acco", "mplishe",
            "s the acti", "vity goal.", "\"", ",\n", " ", "     \"",
            "F", "orma", "t Compli", "anc", "e: Every ", "descr",
            "iption starts ", "with ", "an ", "impera", "tive verb.",
            "\"", ",\n", " ", "     \"", "N", "ame ",
            "Integ", "rity: ", "acti", "vity_n", "ame ", "MUST ",
            "be ", "copied ", "verba", "tim from ", "inpu", "t - ",
            "no ", "modif", "ications allowe", "d.\"", "\n", " ", "   ]",
            "\n", " ", " }", ",\n", " ", " \"",
            "f", "ina", "l_i", "nstru", "ction\": ", "\"P",
            "roce", "ss 'i", "npu", "t.a", "ctivi", "ties'. ", "Apply ",
            "all ", "rules.", " ", "Outp", "ut ONL", "Y a ", "singl",
            "e JSO", "N objec", "t with ", "the ", "key ",
            "\\\"d", "ecom", "po", "sitio", "n_result\\\" ", "contai",
            "ning the ", "array.", " ", "CRIT", "IC", "AL: ", "Every ",
            "acti", "vity_n", "ame ", "in ", "your ", "outpu", "t must ",
            "matc", "h the ", "inpu", "t acti", "vity_n", "ame ", "EXA",
            "CTLY,", " ", "chara", "cter-f", "or-", "c", "hara", "cter. ",
            "No ", "markd", "own, ", "no ", "extra ", "text,",
            " ", "no ", "expla", "nations. ", "Use ", "the ", "exa",
            "mple in ", "'f", "ew_", "s", "hot_", "l", "earni", "ng' ",
            "as ", "a ", "templa", "te for ", "the ", "struc", "ture and ",
            "granu", "larity of ", "subste", "ps.", "\"", "\n", "}"
        ]
    },
    "fragmentation_analysis": {
        "MUST EXACTLY MATCH": {
            "deepseek": {"tokens": 65, "TFI": 21.666666666666668},
            "gemini": {"tokens": 166, "TFI": 55.333333333333336}
        },
        "decomposition_result": {
            "deepseek": {"tokens": 80, "TFI": 80},
            "gemini": {"tokens": 73, "TFI": 73}
        },
        "Do NOT describe": {
            "deepseek": {"tokens": 50, "TFI": 16.666666666666668},
            "gemini": {"tokens": 184, "TFI": 61.333333333333336}
        },
        "observable staff actions": {
            "deepseek": {"tokens": 62, "TFI": 20.666666666666668},
            "gemini": {"tokens": 180, "TFI": 60}
        },
        "HIS": {
            "deepseek": {"tokens": 30, "TFI": 30},
            "gemini": {"tokens": 15, "TFI": 15}
        },
        "scanner": {
            "deepseek": {"tokens": 53, "TFI": 53},
            "gemini": {"tokens": 46, "TFI": 46}
        },
        "printer": {
            "deepseek": {"tokens": 34, "TFI": 34},
            "gemini": {"tokens": 15, "TFI": 15}
        },
        "filing cabinet": {
            "deepseek": {"tokens": 50, "TFI": 25},
            "gemini": {"tokens": 152, "TFI": 76}
        }
    }
}

# ============================================================
# VISUALIZATION CODE
# ============================================================

fig3, axes = plt.subplots(2, 1, figsize=(22, 16))

# Extract token data for a key phrase
phrase_to_analyze = "MUST EXACTLY MATCH"

# DeepSeek tokens around this phrase
ds_tokens = tokenizer_report['deepseek']['tokens']
gg_tokens = tokenizer_report['gemini']['tokens']

# Find indices where phrase appears
ds_phrase_indices = []
for i, t in enumerate(ds_tokens):
    clean = t.replace('Ġ', ' ').replace('Ċ', '\n').lower()
    if any(word in clean for word in ['must', 'exactly', 'match']):
        ds_phrase_indices.append(i)

# For Gemini
gg_phrase_indices = []
for i, t in enumerate(gg_tokens):
    clean = t.lower()
    if any(word in clean for word in ['must', 'exactly', 'match']):
        gg_phrase_indices.append(i)

# Plot 1: DeepSeek token sequence
ax_ds = axes[0]
ds_window_start = max(0, min(ds_phrase_indices) - 5) if ds_phrase_indices else 200
ds_window_end = min(len(ds_tokens), max(ds_phrase_indices) + 10) if ds_phrase_indices else 250
ds_window = ds_tokens[ds_window_start:ds_window_end]

# Create color coding
colors_tokens_ds = []
for t in ds_window:
    clean = t.replace('Ġ', ' ').replace('Ċ', '\n').lower()
    if 'must' in clean or 'exactly' in clean or 'match' in clean:
        colors_tokens_ds.append('#EF4444')  # Red for constraint words
    elif t in ['"', ':', '{', '}', ',', '\n']:
        colors_tokens_ds.append('#9CA3AF')  # Gray for syntax
    else:
        colors_tokens_ds.append('#3B82F6')  # Blue for regular

y_pos = 0
for i, (token, color) in enumerate(zip(ds_window, colors_tokens_ds)):
    display_token = token.replace('Ġ', '>').replace('Ċ', 'N').replace('\n', 'N')
    if len(display_token) > 25:
        display_token = display_token[:22] + '...'

    rect = plt.Rectangle((i * 0.8, y_pos), 0.75, 0.6, facecolor=color, edgecolor='white', linewidth=1)
    ax_ds.add_patch(rect)
    ax_ds.text(i * 0.8 + 0.375, y_pos + 0.3, display_token, ha='center', va='center', 
               fontsize=8, color='white', fontweight='bold', rotation=0)

ax_ds.set_xlim(-0.2, len(ds_window) * 0.8 + 0.2)
ax_ds.set_ylim(-0.2, 1.0)
ax_ds.set_title(f'DeepSeek Token Sequence around "{phrase_to_analyze}" (TFI = 21.67)', 
                fontsize=13, fontweight='bold', pad=10)
ax_ds.axis('off')

# Add legend
legend_elements = [mpatches.Patch(facecolor='#EF4444', label='Constraint words (must/exactly/match)'),
                   mpatches.Patch(facecolor='#3B82F6', label='Regular content'),
                   mpatches.Patch(facecolor='#9CA3AF', label='JSON syntax')]
ax_ds.legend(handles=legend_elements, loc='upper right', fontsize=9)

# Plot 2: Gemini token sequence
ax_gg = axes[1]
gg_window_start = max(0, min(gg_phrase_indices) - 5) if gg_phrase_indices else 200
gg_window_end = min(len(gg_tokens), max(gg_phrase_indices) + 15) if gg_phrase_indices else 280
gg_window = gg_tokens[gg_window_start:gg_window_end]

colors_tokens_gg = []
for t in gg_window:
    clean = t.lower()
    if 'must' in clean or 'exactly' in clean or 'match' in clean:
        colors_tokens_gg.append('#EF4444')
    elif t in ['"', ':', '{', '}', ',', '\n', ' ']:
        colors_tokens_gg.append('#9CA3AF')
    else:
        colors_tokens_gg.append('#3B82F6')

for i, (token, color) in enumerate(zip(gg_window, colors_tokens_gg)):
    display_token = token.replace('\n', 'N')
    if len(display_token) > 30:
        display_token = display_token[:27] + '...'

    rect = plt.Rectangle((i * 0.8, y_pos), 0.75, 0.6, facecolor=color, edgecolor='white', linewidth=1)
    ax_gg.add_patch(rect)
    ax_gg.text(i * 0.8 + 0.375, y_pos + 0.3, display_token, ha='center', va='center', 
               fontsize=7, color='white', fontweight='bold', rotation=0)

ax_gg.set_xlim(-0.2, len(gg_window) * 0.8 + 0.2)
ax_gg.set_ylim(-0.2, 1.0)
ax_gg.set_title(f'Gemini Token Sequence around "{phrase_to_analyze}" (TFI = 55.33)', 
                fontsize=13, fontweight='bold', pad=10)
ax_gg.axis('off')
ax_gg.legend(handles=legend_elements, loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('token_comparison_heatmap.png', dpi=200, bbox_inches='tight', facecolor='white')
print("Token comparison heatmap saved to token_comparison_heatmap.png")