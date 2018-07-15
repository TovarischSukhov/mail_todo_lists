# encoding=utf-8

FACTS = '''
import "base.proto";
import "facttypes_base.proto";

{}
'''

KEYWORDS = '''
import "base.proto";
import "articles_base.proto"; 

{}
'''

GAZETTEER = '''
encoding "utf8";
import "base.proto";
import "articles_base.proto";
import "kwtypes.proto";
import "facttypes.proto";

{}
'''

MAIN_CONFIG = '''
encoding "utf8";

TTextMinerConfig {{
    Dictionary = "dict.gzt";
    Input = {{
        File = "documents_dlp.txt"; // файл с анализируемым текстом
        Type = dpl;                 // режим чтения
    }}

    // Articles and Facts begins:
    {config}
    
    NumThreads = {num_threads};
    
    Output = {{
        File = "facts.xml";
    }}
}}
'''

FACT_BODY = '''
#encoding "utf-8" 
{}
'''
