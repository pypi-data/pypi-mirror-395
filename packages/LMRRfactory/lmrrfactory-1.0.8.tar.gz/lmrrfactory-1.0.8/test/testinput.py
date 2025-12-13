# python "test/testinput.py"
from LMRRfactory import makeYAML

models = {
    'Think': 'test/data/think.yaml'
    }

for m in models.keys():
    # makeYAML(mechInput=models[m],
    #          outputPath='test/outputs/Dec27')
    makeYAML(mechInput=models[m],
             outputPath='test/outputs/Dec27',
             allPdep=True)
    # makeYAML(mechInput=models[m],
    #          outputPath='test/outputs/Dec27',
    #          allPLOG=True)