import yaml
import numpy as np
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
import copy
from collections import Counter
import re
import os
from importlib.resources import files
import cantera as ct
import warnings
import io

warnings.filterwarnings("ignore")

class makeYAML:
    def __init__(self,mechInput, colliderInput=None, outputPath=".", allPdep=False):
        self.T_ls = None
        self.P_ls = None
        self.n_P= None
        self.n_T= None
        self.P_min = None
        self.P_max = None
        self.T_min = None
        self.T_max = None
        self.rxnIdx = None
        self.colliderInput=None
        self.units = self._loadYAML(mechInput).get("units",{})
        self.allPdep = False # option to apply generic 3b-effs to all p-dep rxns in mech
        self.input = self._loadYAML(colliderInput) if colliderInput else None
        self.mechInput = mechInput
        os.makedirs(outputPath,exist_ok=True)
        self.foutName = f"{outputPath}/{os.path.basename(self.mechInput).replace(".yaml","_LMRR")}"
        if allPdep:
            self.allPdep = True
            self.foutName = f"{self.foutName}_allP"
        self.mech_obj = ct.Solution(mechInput)
        self._lookForPdep() # Verify that 'mech' has >=1 relevant p-dep reaction
        self.mech_pes = self._getPES()
        self.defaults = self._loadYAML(f"{str(files("LMRRfactory"))}/thirdbodydatabase.yaml")
        self._normalizedKeys() # normalize species as uppercase
        self.species_dict = {}
        for sp in self.mech_obj.species():
            self.species_dict[sp.name.upper()] = dict(sp.composition.items())
        # Remove defaults colliders and reactions that were explictly provided by user
        self._deleteDuplicates()
        # Blend the user inputs and remaining collider defaults into a single YAML
        self.blend = self._blendedInput()
        # Sub the colliders into their corresponding reactions in the input mechanism
        self.output = self._zippedMech()
        # self.validate()
        self._saveYAML()
        print(f"LMR-R mechanism successfully generated and stored at "
            f"{self.foutName}.yaml")

    def _normalizedKeys(self):
        def capitalize(dict):
            return {k.capitalize(): v for k, v in dict.items()}
        for defaultRxn in self.defaults['reactions']:
            for col in defaultRxn['colliders']:
                col['composition'] = capitalize(col['composition'])
            defaultRxn['reference-collider'] = defaultRxn['reference-collider'].upper()
            defaultRxn['pes'] = capitalize(defaultRxn['pes'])
        if self.input and self.input.get('reactions'):
            for inputRxn in self.input['reactions']:
                for col in inputRxn['colliders']:
                    col['composition'] = capitalize(col['composition'])
                inputRxn['reference-collider'] = inputRxn['reference-collider'].upper()
                inputRxn['pes'] = capitalize(inputRxn['pes'])

    def _lookForPdep(self):
        if not any(
            reaction.reaction_type in ['falloff-Troe','pressure-dependent-Arrhenius', 'Chebyshev', 'three-body-linear-Burke']
            for reaction in self.mech_obj.reactions()
        ):
            raise ValueError("No pressure-dependent reactions found in mechanism."
                            " Please choose another mechanism.")
    
    def _getPES(self): #must input an equation that has already been normalized
        pes=[]
        for reaction in self.mech_obj.reactions():
            compositions = []
            reactant_species = list(reaction.reactants.keys())
            reactant_coeffs = list(reaction.reactants.values())
            for i, reactant in enumerate(reactant_species):
                spec = self.mech_obj.species(reactant)
                c = spec.composition
                c_scaled = {k.upper(): v*reactant_coeffs[i] for k, v in c.items()}
                compositions.append(c_scaled)
            counters = [Counter(comp) for comp in compositions]
            pes.append(sum(counters, Counter()))
        return pes

    def _deleteDuplicates(self): # delete duplicates from thirdbodydatabase
        newData = {'generic-colliders': self.defaults['generic-colliders'],
                'reactions': []}
        inputRxnNames = None
        if self.input:
            if self.input.get('reactions'):
                inputRxnNames = [rxn['pes'] for rxn in self.input['reactions']]
                inputColliderNames = [[col['composition'] for col in rxn['colliders']]
                                    for rxn in self.input['reactions']]
        for defaultRxn in self.defaults['reactions']:
            if inputRxnNames and defaultRxn['pes'] in inputRxnNames:
                idx = inputRxnNames.index(defaultRxn['pes'])
                inputColliders = inputColliderNames[idx]
                newColliderList = [col for col in defaultRxn['colliders']
                                if col['composition'] not in inputColliders]
                if len(newColliderList)>0:
                    newData['reactions'].append({
                        'name': defaultRxn['name'],
                        'pes': defaultRxn['pes'],
                        'reference-collider': defaultRxn['reference-collider'],
                        'colliders': newColliderList
                    })
            else: # reaction isn't in input, so keep the entire default rxn
                newData['reactions'].append(defaultRxn)
        self.defaults=newData

    

    def _blendedInput(self):
        blendData = {'reactions': []}
        
        # first fill it with all of the default reactions and colliders (which have valid species)
        for defaultRxn in self.defaults['reactions']:
            newCollList = []
            for col in defaultRxn['colliders']:
                if col['composition'] in list(self.species_dict.values()):
                    newCollList.append(col)
            defaultRxn['colliders'] = newCollList
            blendData['reactions'].append(defaultRxn)
        defaultRxnNames = [rxn['pes'] for rxn in blendData['reactions']]
        if self.input:
            if self.input.get('reactions'):
                for inputRxn in self.input['reactions']:
                    # Check if input reaction also exists in defaults file, otherwise add the entire input reaction to the blend as-is
                    if inputRxn['pes'] in defaultRxnNames:
                        idx = defaultRxnNames.index(inputRxn['pes'])
                        blendRxn = blendData['reactions'][idx]
                        # If reference colliders match, append new colliders, otherwise override with the user inputs
                        if inputRxn['reference-collider'] == blendRxn['reference-collider']:
                            newColliders = [col for col in inputRxn['colliders']
                                            if col['composition'] in list(self.species_dict.values())]
                            blendRxn['colliders'].extend(newColliders)
                        else:
                            print(f"User-provided reference collider for {inputRxn['equation']}, "
                                f"({inputRxn['reference-collider']}) does not match the program "
                                f"default ({blendData['reactions'][idx]['reference-collider']})."
                                f"\nThe default colliders have thus been deleted and the reaction"
                                f" has been completely overrided by (rather than blended with) "
                                f"the user's custom input values.")
                            blendRxn['reference-collider'] = inputRxn['reference-collider']
                            newColliders = [col for col in inputRxn['colliders']
                                            if col['composition'] in list(self.species_dict.values())]
                            blendRxn['colliders'] = newColliders
                            # blendRxn['colliders'] = inputRxn['colliders']
                    else:
                        if all(col['composition'] in list(self.species_dict.values()) for col in inputRxn['colliders']):
                            blendData['reactions'].append(inputRxn)
        return blendData

    def _to_builtin(self,obj):
        if isinstance(obj, dict):
            return {self._to_builtin(k): self._to_builtin(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._to_builtin(i) for i in obj]
        elif hasattr(obj, 'as_dict'):
            return self._to_builtin(obj.as_dict())
        elif hasattr(obj, '__dict__'):
            return self._to_builtin(vars(obj))
        elif hasattr(obj, 'tolist'):  # NumPy arrays or similar
            return obj.tolist()
        else:
            return obj

    def _arrheniusFit(self,temps,eps):
        temps = np.asarray(temps, dtype=float)
        eps = np.asarray(eps, dtype=float)
        # ln(eps) = ln A + b*ln(T) - (Ea/R)*(1/T)
        y = np.log(eps)
        X = np.column_stack([np.ones_like(temps),np.log(temps),1/temps])
        if len(temps) == 2:
            c0, c1 = np.linalg.lstsq(X[:, :2], y, rcond=None)[0]
            A, b, Ea = float(np.exp(c0)), float(c1), 0.0
        else:
            c0, c1, c2 = np.linalg.lstsq(X, y, rcond=None)[0]
            A, b, Ea = round(float(np.exp(c0)),8), round(float(c1),8), round(float(-c2*ct.gas_constant),8)
        return {'A': A,'b': b,'Ea': Ea}
    
    def _rescaleArrhenius(self,k_ref,k_i):
        A_new = k_i['A']/k_ref['A']
        b_new = k_i['b']-k_ref['b']
        Ea_new = k_i['Ea']-k_ref['Ea']
        return {'A': A_new,'b': b_new,'Ea': Ea_new}

    def _colliders(self,mech_rxn,blend_rxn=None,generic=False):
        divisor = 1
        colliders=[]
        colliderNames=[]
        is_M_N2 = False
        troe_efficiencies={}
        if mech_rxn.reaction_type == 'falloff-Troe':
            troe_efficiencies= mech_rxn.input_data.get('efficiencies', {})
            # for sp_name in list(troe_efficiencies_raw.keys()):
            #     # [disregard] make the keys the compositions instead of species names
            #     troe_efficiencies[sp_name] = troe_efficiencies_raw[sp_name]
        elif mech_rxn.reaction_type == 'three-body-linear-Burke': #case where we've used the linear Burke format so that Troe params can be used alongside a PLOG 
            # for c, col in enumerate(mech_rxn.input_data.get('colliders', {})):
            #     if col['name'].upper() == 'AR':
            for c, col in enumerate(mech_rxn.input_data.get('colliders', {})):
                if c>0 and col['efficiency']['b']==0 and col['efficiency']['Ea']==0:
                    troe_efficiencies[col['name']]=col['efficiency']['A'] ## WHY ARE WE USING TROE EFFICIENCIES HERE
        for name, val in troe_efficiencies.items():
            comp = self.species_dict[name.upper()]
            # Check if N2 is the reference collider instead of Ar
            if comp=={'Ar': 1} and val!=0 and val !=1:
                is_M_N2 = True
                divisor = 1/val
        for name, val in troe_efficiencies.items():
            comp = self.species_dict[name.upper()]
            if is_M_N2 and comp=={'N': 2} and val!=0 and val !=1:
                is_M_N2 = False #just treat as if Ar is reference since case is ambiguous
                print(f"> Warning: {mech_rxn} has both Ar and N2 as non-unity colliders! Please fix.")
            if comp=={'Ar': 1} and val==0 :
                print(f"> Warning: {mech_rxn} has Ar assumed as reference collider, since params cannot be scaled by the Ar=0 value provided. Please fix.")
        if is_M_N2:
            if blend_rxn:
                for col in blend_rxn['colliders']:
                    if col['composition']=={'N': 2}:
                        k_ref = self._arrheniusFit(col['temperatures'],col['efficiency'])
                for col in blend_rxn['colliders']:
                    newCol = copy.deepcopy(col)
                    k_i = None
                    #Convert N2:Ar database entry to Ar:N2
                    if newCol['composition']=={'N': 2}:
                        newCol['composition']={'Ar': 1}
                        newCol['name']=next(k for k, v in self.species_dict.items() if v == newCol['composition'])
                        k_i = self._arrheniusFit([300,1000,2000],[1,1,1])
                    elif newCol['composition'] in list(self.species_dict.values()):
                        k_i = self._arrheniusFit(col['temperatures'],col['efficiency'])
                    if k_i:
                        newCol['efficiency']=self._rescaleArrhenius(k_ref,k_i)
                        colliderNames.append(newCol['composition'])
                        colliders.append(newCol)
                    
            # Add troe efficiencies that haven't already been given a value
            for name, val in troe_efficiencies.items():
                comp = self.species_dict[name.upper()]
                already_given = comp in colliderNames
                if not already_given and not comp=={'N': 2}: #ignores the redundant n2=1 entry
                    colliders.append({
                        'name': next(k for k, v in self.species_dict.items() if v == comp),
                        'efficiency': {'A':val,'b':0,'Ea':0 },
                        'note': 'present work',
                    })
                    colliderNames.append(self.species_dict[name.upper()])
            if generic:
                for col in self.defaults['generic-colliders']:
                    already_given = col['composition'] in colliderNames
                    if col['composition'] in list(self.species_dict.values()) and not already_given and not col['composition']=={'N': 2}:
                        colliders.append({
                            'name': next(k for k, v in self.species_dict.items() if v == col['composition']),
                            'efficiency': {'A': col['efficiency']/divisor,'b':0,'Ea':0},
                            'note': col['note']
                        })
        else:
            if blend_rxn:
                # Make reaction-specific colliders wrt Ar and append to collider list 
                for col in blend_rxn['colliders']:
                    if col['composition'] in list(self.species_dict.values()):
                        newCol = copy.deepcopy(col)
                        newCol['efficiency']=self._arrheniusFit(newCol['temperatures'], newCol['efficiency'])
                        colliderNames.append(newCol['composition'])
                        colliders.append(newCol)
            # Add troe efficiencies that haven't already been given a value
            for name, val in troe_efficiencies.items():
                comp = self.species_dict[name.upper()]
                # already_given = any(col['name'] == name for col in colliders)
                already_given = comp in colliderNames
                if not already_given and not comp=={'Ar': 1}:
                    colliders.append({
                        'name': next(k for k, v in self.species_dict.items() if v == comp),
                        'efficiency': {'A':val,'b':0,'Ea':0 },
                        'note': 'present work',
                    })
                    colliderNames.append(comp)
            if generic:
                for col in self.defaults['generic-colliders']:
                    already_given = col['composition'] in colliderNames
                    if col['composition'] in list(self.species_dict.values()) and not already_given and not col['composition']=={'Ar': 1}:
                        colliders.append({
                            'name': next(k for k, v in self.species_dict.items() if v == col['composition']),
                            'efficiency': {'A': col['efficiency'],'b':0,'Ea':0},
                            'note': col['note']
                        })
        # for col in colliders:
        #     col.pop('composition',None)
        #     col.pop('temperatures', None)
        return colliders

    def _zippedMech(self):
        
        newReactions = []
        blendRxnNames = [rxn['pes'] for rxn in self.blend['reactions']]
        for i, mech_rxn in enumerate(self.mech_obj.reactions()):
            pDep = False
            # Create the M-collider entry for the pressure-dependent reactions
            if mech_rxn.reaction_type in ['falloff-Troe','three-body-pressure-dependent-Arrhenius','pressure-dependent-Arrhenius','Chebyshev','three-body-linear-Burke']:     
                pDep = True
                if mech_rxn.reaction_type == 'three-body-linear-Burke':
                    d = self._to_builtin(mech_rxn.input_data['colliders'][0]) #use the pdep format given for collider M when rebuilding the reaction
                    d.pop("name")
                else:
                    d = self._to_builtin(mech_rxn.input_data)
                    d.pop("equation")
                    d.pop("efficiencies",None) #only applies to Troe reactions
                d.pop("duplicate", None)
                d.pop("units", None)
                if d.get('Troe'):
                    d['Troe']=dict(d['Troe'])
                if d.get('low-P-rate-constant'):
                    d['low-P-rate-constant']=dict(d['low-P-rate-constant'])
                if d.get('high-P-rate-constant'):
                    d['high-P-rate-constant']=dict(d['high-P-rate-constant'])
                colliderM = {'name': 'M'}
                colliderM.update(dict(d))
            if pDep and (self.mech_pes[i] in blendRxnNames or self.allPdep):
                genericBool = True if self.allPdep else False
                blendRxn = None
                if self.mech_pes[i] in blendRxnNames:
                    # rxn is specifically covered either in defaults or user input
                    idx = blendRxnNames.index(self.mech_pes[i])
                    blendRxn = self.blend['reactions'][idx]
                if blendRxn and not genericBool:
                    param_type = "ab initio"
                elif genericBool and not blendRxn:
                    param_type = "generic"
                elif blendRxn and genericBool:
                    param_type = "ab initio and generic"
                colliders = self._colliders(mech_rxn,blend_rxn=blendRxn, generic=genericBool)
                d = self._to_builtin(mech_rxn.input_data)
                newRxn = {
                    'equation': mech_rxn.equation,
                    **({'duplicate': True} if d.get('duplicate') else {}),
                    **({'units': d['units']} if d.get('units') else {}),
                    'type': 'linear-Burke',
                    'colliders': [colliderM] + colliders
                }
                if 'note' in d and re.fullmatch(r'\n+', d['note']):
                    newRxn['note'] = ''
                yaml_str = yaml.dump(newRxn, sort_keys=False)
                newRxn_obj = ct.Reaction.from_yaml(yaml_str,self.mech_obj)
                newReactions.append(newRxn_obj)
                print(f"{mech_rxn} {dict(self.mech_pes[i])} converted to LMR-R with {param_type} parameters.")
            else: # just append it as-is
                d = mech_rxn.input_data
                if 'note' in d and re.fullmatch(r'\n+', d['note']):
                    mech_rxn.update_user_data({'note': ''})
                newReactions.append(mech_rxn)
        output_data = {
            'thermo': self.mech_obj.thermo_model,
            'kinetics': self.mech_obj.kinetics_model,
            'transport_model': self.mech_obj.transport_model,
            'species': self.mech_obj.species(),
            'reactions': newReactions,
            'name': 'gas',
        }
        return ct.Solution(**output_data)

    def _loadYAML(self, fName):
        with open(fName) as f:
            return yaml.safe_load(f)
    
    def _saveYAML(self):
        fName = f"{self.foutName}.yaml"
        self.output.write_yaml(filename=fName, units=self.units)
        # Resave it to remove formatting inconsistencies
        mech = self._loadYAML(fName)
        # Prevent 'NO' from being misinterpreted as bool in species list
        mech['phases'][0]['species'] = [
            "NO" if str(molec).lower() == "false" else molec
            for molec in mech['phases'][0]['species']
        ]
        for species in mech['species']:
            if str(species['name']).lower() == "false":
                species['name']="NO"
        
        for reaction in mech['reactions']:
            if reaction.get('efficiencies'):
                # Prevent 'NO' from being misinterpreted as bool in efficiencies list found in Troe falloff reactions
                reaction['efficiencies'] = {
                    "NO" if str(key).lower() == "false" else key: reaction['efficiencies'][key]
                    for key in reaction['efficiencies']
                }
            if reaction.get('colliders'):
                for col in reaction['colliders']:
                    if str(col['name']).lower() == "false":
                        col['name']="NO"

        # Prevent 'NO' from being misinterpreted as bool in colliders list for LMRR rxns
        for reaction in mech['reactions']:
            effs = reaction.get('efficiencies')
            if effs:
                reaction['efficiencies'] = {
                    "NO" if str(key).lower() == "false" else key: effs[key]
                    for key in effs
                }
        with open(fName, 'w') as outfile:
            yaml.safe_dump(copy.deepcopy(mech), outfile,
            default_flow_style=None,
            sort_keys=False)
       

## VALIDATION OF INTERNAL DBASE
# All temp/eps pairs must be of matching length