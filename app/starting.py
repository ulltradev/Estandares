import json

config = {}
config['rutaEntrada'] = ''
config['formatos'] = []
config['columnas'] = []
config['noRFormatos'] = []
config['columnasNoVacias'] = []
config['formatos'].append({
    'nombre':'nombreDeFormato',
    'determinadorDeFormato': r'palabraimporsibledeaparecerentexto',
    'separadorDeEventos': r'palabraimporsibledeaparecerentexto',
    'variables':[{
                    'talla':r'regexdetalla'
    },{
                    'peso':r'regexdepeso'
    }],
    'eliminables':[{
                    'talla':['cm','kg']
    },{
                    'peso':['kg','mg']
    }]
})

with open('config.txt','w') as outfile:
    json.dump(config,outfile)