from enum import Enum
from math import isnan
from typing import Callable, Optional, Iterator, Literal

from rdflib.plugins.sparql.algebra import analyse
from requests import Response

from chemotion_api.elements.abstract_element import AbstractElement, Analyses, AnalysesList, Segments, Segment
from datetime import datetime

from chemotion_api.elements.sample import Sample, SampleVariationType, GasPhaseObj
from chemotion_api.elements.utils import QuantityUnit, GasType
from chemotion_api.elements.schemas.reaction import schema, PURIFICATION_OPTIONS, STATUS_OPTIONS
from chemotion_api.elements.utils.converter import convert_value_to_default, VOLUME_UNITS, convert_value
from chemotion_api.generic_segments import GenericSegments
from chemotion_api.labImotion.items.options import FieldType
from chemotion_api.utils import TypedList, quill_hedging, merge_dicts, PropertyDict, UnitDict
from collections.abc import MutableSequence


class MaterialList(TypedList):
    """
    A list which accepts only :class:`chemotion_api.elements.sample.Sample`'s.
    If you add a sample using th standard list-methods a splited sample will be created.
    Then the created sample will be added to the list.
    If the element has no ID, it will be saved.

    In order to avoid the splitting and the pre saving use the 'append_no_split'
    methode.
    """

    def __init__(self, reaction: 'Reaction',
                 mat_type: Literal['starting_materials', 'reactants', 'products', 'solvents', 'purification_solvents'],
                 *args):
        super().__init__(Sample, *args)
        self._reaction = reaction
        self._mat_type = mat_type

    def _prepare_element(self, element: Sample):
        if self._mat_type == 'starting_materials':
            return_element = element.split()
        elif self._mat_type == 'reactants':
            return_element = element.split()
            return_element.properties['short_label'] = 'reactant'
        elif self._mat_type == 'products':
            return_element = element.copy()
        elif self._mat_type == 'solvents':
            return_element = element
        elif self._mat_type == 'purification_solvents':
            return_element = element
        else:
            raise ValueError("Unknown material type.")
        return_element.reaction = self._reaction
        return_element.role_in_reaction = self._mat_type
        return_element.set_ref(False, False)
        return_element.properties['position'] = len(self)

        return return_element

    def after_append(self, element: Sample):
        try:

            element.set_amount(**element.get_amount())
        except ValueError or KeyError:
            element.set_amount(0, element.allowed_quantity_units()[0])

    def append_no_split(self, element: Sample):
        """
        Add a Sample without splitting it
        :param element: Sample to be added
        """

        self._check_element(element)
        return super(TypedList, self).append(element)


class Temperature(dict):
    """
    This object contains the  temperature-time profile, the temperature unit and a user text.
    Each entry contains a time as 'hh:mm:ss' and a temperature as integer.

    :key data: {list} the temperature-time profile
    :key userText: {str}
    :key valueUnit: {str}
    """

    def __init__(self, **kwargs):
        super().__init__(data=kwargs.get('data', []),
                         userText=kwargs.get('userText', ''),
                         valueUnit=kwargs.get('valueUnit', "°C")
                         )

    def add_time_point(self, hour: int, minute: int, second: int, temperature: float):
        """
        Adds an entry to the Temperature timeline

        :param hour: since the reaction has started
        :param minute: since the reaction has started
        :param second: since the reaction has started
        :param temperature: degrees
        """
        data = self.get('data')
        if data is None:
            self['data'] = []
            data = self['data']
        data.append(
            {'time': f'{str(hour).zfill(2)}:{str(minute).zfill(2)}:{str(second).zfill(2)}', 'value': str(temperature)})


class Reaction(AbstractElement):
    """
    A chemotion Reaction object.
    It extends the :class:`chemotion_api.elements.abstract_element.AbstractElement`

    Usage::

    >>> from chemotion_api import Instance
    >>> from chemotion_api.collection import Collection
    >>> import logging
    >>> try:
    >>>     instance = Instance('http(d)://xxx.xxx.xxx').test_connection().login('<USER>', "<PASSWORD>")
    >>> except ConnectionError as e:
    >>>     logging.error(f"A connection to Chemotion ({instance.host_url}) cannot be established")
    >>> # Get the reaction with ID 1
    >>> rea = instance.get_reaction(1)
    >>> # Set the real amount to 3.7 g
    >>> col_solv: Collection = instance.get_root_collection().get_or_create_collection('Solv')
    >>> # Create a new solvent CDCl3
    >>> solv = col_solv.new_solvent('CDCl3')
    >>> # Add CDCl3 as solvent to the reaction
    >>> rea.solvents.append(solv)
    >>> # Add a split of sample with ID 1 as starting material
    >>> rea.starting_materials.append(instance.get_sample(1))
    >>> # Add a new time/temperature step to the temperature timeline
    >>> rea.properties['temperature'].add_time_point(2,3,0,100)
    >>> rea.save()
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._variations = None

    datetime_format = '%m/%d/%Y %H:%M:%S'

    def _set_json_data(self, json_data: dict):
        super()._set_json_data(json_data)
        self._svg_file = self.json_data.get('reaction_svg_file')

    def load_image(self) -> Response:
        """
        Loads the reaction structure as svg image

        :return: Response with the svg as content
        """

        image_url = "/images/reactions/{}".format(self._svg_file)
        res = self._session.get(image_url)
        if res.status_code != 200:
            raise ConnectionError('{} -> {}'.format(res.status_code, res.text))
        return res

    def properties_schema(self) -> dict:
        """
        Returns the JSON.org schema of the cleaned properties.

        :return: JSON.org schema
        """

        return schema

    @property
    def properties(self) -> PropertyDict:
        """
        The properties property contains all data which can be altered
        through the chemotion api from the main tab of the reaction.


        :key starting_materials: {:class:`chemotion_api.elements.reaction.MaterialList`}
        :key reactants:  {:class:`chemotion_api.elements.reaction.MaterialList`}
        :key products: {:class:`chemotion_api.elements.reaction.MaterialList`}
        :key solvents: {:class:`chemotion_api.elements.reaction.MaterialList`}
        :key purification_solvents: {:class:`chemotion_api.elements.reaction.MaterialList`}
        :key temperature: {:class:`chemotion_api.elements.reaction.Temperature`}
        :key timestamp_start: {datetime.datetime}
        :key timestamp_stop: {datetime.datetime}
        :key name: {str}
        :key description: {str|dict} A Guill.js text (https://quilljs.com/docs/delta)
        :key observation: {str|dict} A Guill.js text (https://quilljs.com/docs/delta)
        :key purification: {list[str]} values must be in ['Flash-Chromatography', 'TLC', 'HPLC', 'Extraction', 'Distillation', 'Dialysis', 'Filtration', 'Sublimation', 'Crystallisation', 'Recrystallisation', 'Precipitation']
        :key status: {str} value must be in ['', 'Planned', 'Running', 'Done', 'Analyses Pending', 'Successful',
                                          'Not Successful']
        :key vessel_size: {dict} has a unit {str} ('l' or 'ml') and an amount {float}

        Readonly properties:

        :key short_label: {str, readonly}
        :key tlc_solvents: {str, readonly}
        :key tlc_description: {str, readonly}
        :key reaction_svg_file: {str, readonly}
        :key role: {str, readonly}
        :key rf_value: {str, readonly}
        :key rxno: {str, readonly}
        :key literatures: {str, readonly}
        :key variations: {str, readonly} Can be used with the reaction class property variations

        :return: Element properties
        """
        return super().properties

    @property
    def vessel_size_in_l(self):
        if self.properties['vessel_size']['amount'] is None:
            return 0
        return convert_value_to_default(unit=self.properties['vessel_size']['unit'],
                                        value=self.properties['vessel_size']['amount'])

    @property
    def variations(self) -> 'Variations':
        if self._variations is None:
            self._variations = Variations(self)

        return self._variations

    @property
    def starting_materials(self) -> MaterialList:
        return self.properties['starting_materials']

    @property
    def reactants(self) -> MaterialList:
        return self.properties['reactants']

    @property
    def products(self) -> MaterialList:
        return self.properties['products']

    @property
    def solvents(self) -> MaterialList:
        return self.properties['solvents']

    @property
    def purification_solvents(self) -> MaterialList:
        return self.properties['purification_solvents']

    @property
    def reference_sample(self) -> Optional[Sample]:
        first_sample = None
        for mat in [*self.starting_materials, *self.reactants]:
            if first_sample is None:
                first_sample = mat
            if mat.properties['reference']:
                return mat
        if mat is not None:
            mat.properties['reference'] = True
        return mat

    @reference_sample.setter
    def reference_sample(self, value: Sample | None):
        id = None if value is None else value.id
        for mat in [*self.starting_materials, *self.reactants]:
            mat.set_ref(mat.id == id, False)
        for mat in [*self.products, *self.solvents, *self.purification_solvents]:
            mat.set_ref(mat.id == id, False)
        self.update_equivalent()

    @property
    def gas_schema(self) -> bool:
        return self._properties.get('gaseous', False)

    @gas_schema.setter
    def gas_schema(self, gaseous: bool):
        self._properties['gaseous'] = gaseous
        if not gaseous:
            for mat in [*self.starting_materials, *self.reactants, *self.products, *self.solvents,
                        *self.purification_solvents]:
                mat.set_gas_type('off', False)
        self.update_equivalent()

    def get_feedstock(self) -> Sample | None:
        return self.get_gas_component(GasType.FEEDSTOCK)

    def get_catalyst(self) -> Sample | None:
        return self.get_gas_component(GasType.CATALYST)

    def get_gas_component(self, gt: GasType):
        if self.gas_schema:
            for mat in [*self.starting_materials, *self.reactants]:
                if mat.gas_type == gt:
                    return mat
        return None

    def update_amount(self):
        for mat in [*self.starting_materials, *self.reactants, *self.products, *self.solvents,
                    *self.purification_solvents]:
            mat.update_amount()
        for var in self.variations:
            var.update_amount()

    def update_equivalent(self):
        for mat in [*self.starting_materials, *self.reactants, *self.products, *self.solvents,
                    *self.purification_solvents]:
            mat.update_equivalent()
        for var in self.variations:
            var.update_equivalent()

    def _parse_properties(self) -> dict:
        reaction_elements = {}
        for reaction_elm_names in ['starting_materials', 'reactants', 'products', 'solvents', 'purification_solvents']:
            obj_list = self.json_data[reaction_elm_names]
            temp = []
            for sample in obj_list:
                sample_obj = Sample(self._generic_segments, self._session, sample)
                sample_obj.reaction = self
                temp.append(sample_obj)
            reaction_elements[reaction_elm_names] = MaterialList(self, reaction_elm_names, temp)

        try:
            timestamp_start = datetime.strptime(self.json_data.get('timestamp_start'), self.datetime_format)
        except:
            timestamp_start = None
        try:
            timestamp_stop = datetime.strptime(self.json_data.get('timestamp_stop'), self.datetime_format)
        except:
            timestamp_stop = None
        return reaction_elements | {
            'timestamp_start': timestamp_start,
            'timestamp_stop': timestamp_stop,
            'description': self.json_data.get('description'),
            'name': self.json_data.get('name'),
            'observation': self.json_data.get('observation'),
            'purification': self.json_data.get('purification'),
            'dangerous_products': self.json_data.get('dangerous_products'),
            'conditions': self.json_data.get('conditions'),
            'rinchi_long_key': self.json_data.get('rinchi_long_key'),
            'rinchi_web_key': self.json_data.get('rinchi_web_key'),
            'rinchi_short_key': self.json_data.get('rinchi_short_key'),
            'duration': self.json_data.get('duration'),
            'rxno': self.json_data.get('rxno'),
            'temperature': Temperature(**self.json_data.get('temperature', {})),
            'status': self.json_data.get('status'),
            'vessel_size': self.json_data.get('vessel_size'),
            'gaseous': self.json_data.get('gaseous')
            # 'tlc_solvents': self.jreaction.properties['reactants']son_data.get('tlc_solvents'),
            # 'tlc_description': self.json_data.get('tlc_description'),
            # 'rf_value': self.json_data.get('rf_value'),
        }

    def _clean_properties_data(self, serialize_data: dict | None = None) -> dict:
        if serialize_data is None:
            serialize_data = {}
        serialize_data['materials'] = {}
        for reaction_elm_names in ['starting_materials', 'reactants', 'products', 'solvents', 'purification_solvents']:
            temp_json_sample = self.json_data[reaction_elm_names]
            serialize_data['materials'][reaction_elm_names] = []
            for sample in self.properties[reaction_elm_names]:
                origen = next((x for x in temp_json_sample if x['id'] == sample.id), {})
                serialize_data['materials'][reaction_elm_names].append(origen | sample.clean_data())

        try:
            timestamp_start = self.properties.get('timestamp_start').strftime(self.datetime_format)
        except:
            timestamp_start = ''
        try:
            timestamp_stop = self.properties.get('timestamp_stop').strftime(self.datetime_format)
        except:
            timestamp_stop = ''
        serialize_data['name'] = self.properties.get('name')
        serialize_data['description'] = quill_hedging(self.properties.get('description'), 'Description')
        serialize_data['dangerous_products'] = self.properties.get('dangerous_products')
        serialize_data['conditions'] = self.properties.get('conditions')
        serialize_data['duration'] = self.properties.get('duration')
        serialize_data |= self._calc_duration()
        serialize_data['timestamp_start'] = timestamp_start
        serialize_data['timestamp_stop'] = timestamp_stop
        serialize_data['temperature'] = self.properties.get('temperature')
        serialize_data['observation'] = quill_hedging(self.properties.get('observation'), 'Observation')

        serialize_data['status'] = self.properties.get('status')
        if self.properties.get('status') in STATUS_OPTIONS:
            serialize_data['status'] = self.properties.get('status')
        else:
            serialize_data['status'] = self.json_data.get('status')

        if self.properties.get('purification') is list:
            serialize_data['purification'] = [x for x in self.properties.get('purification') if
                                              x in PURIFICATION_OPTIONS]
        else:
            serialize_data['purification'] = self.json_data.get('purification')

        if self.properties.get('vessel_size') is not None:
            serialize_data['vessel_size'] = self.properties.get('vessel_size')

        serialize_data['role'] = self.properties.get('role', '')
        serialize_data['gaseous'] = self.properties.get('gaseous')
        serialize_data['tlc_solvents'] = self.json_data.get('tlc_solvents')
        serialize_data['tlc_description'] = self.json_data.get('tlc_description')
        serialize_data['reaction_svg_file'] = self.json_data.get('reaction_svg_file')

        serialize_data['rf_value'] = self.json_data.get('rf_value')
        serialize_data['rxno'] = self.json_data.get('rxno', '')
        serialize_data['short_label'] = self.json_data.get('short_label')
        serialize_data['literatures'] = self.json_data.get('literatures')

        serialize_data['research_plans'] = self.json_data.get('research_plans')
        serialize_data['user_labels'] = self.json_data.get('user_labels')
        serialize_data['solvent'] = self.json_data.get('solvent')

        serialize_data['variations'] = self._clean_variations()

        return serialize_data

    def _calc_duration(self):
        a, b = self.properties.get('timestamp_stop'), self.properties.get('timestamp_start')
        if not isinstance(a, datetime) or not isinstance(b, datetime):
            return {
                'durationDisplay': self.json_data.get('durationDisplay'),
                'durationCalc': self.json_data.get('durationCalc')
            }
        c = a - b

        h = int(c.seconds / (60 * 60))
        m = int(c.seconds % (60 * 60) / 60)
        s = c.seconds % 60
        text = []
        total_unit = None
        total_time = 0
        total_factor = 0
        for (time, unit, factor) in ((c.days, 'day', 1), (h, 'hour', 24), (m, 'minute', 60), (s, 'second', 60)):
            total_factor *= factor
            if time > 0:
                if total_unit is None:
                    total_unit = unit + "(s)"
                    total_factor = 1
                total_time += time / total_factor
                text.append(f"{time} {unit}{'s' if time > 1 else ''}")
        return {'durationCalc': ' '.join(text),
                'durationDisplay': {
                    "dispUnit": total_unit,
                    "dispValue": f"{int(total_time)}",
                    "memUnit": total_unit,
                    "memValue": "{:0.15f}".format(total_time)
                }
                }

    def on_properties_change(self, dict_obj, name, value):
        if name[-1] == 'gaseous':
            self.gas_schema = value[-1]
            return False
        if name[-1] == 'vessel_size':
            if len(name) > 1:
                dict_obj[-1][name[-1]] = value[-1]
            elif isinstance(value[-1], int or float):
                dict_obj[-1][name[-1]]['amount'] = value[-1]
            elif VOLUME_UNITS(value[-1]):
                dict_obj[-1][name[-1]]['unit'] = value[-1]
            self.update_amount()
            return False
        return True

    def _clean_variations(self) -> list:
        cleand_data = self.variations.clean()
        self._variations = None
        return cleand_data


class SampleVariation(Sample):

    def __init__(self, reaction: Reaction, sample: Sample, variation_data: dict):
        params = sample.copy_params()
        params['avoid_load'] = True
        super().__init__(**params)
        if variation_data is None:
            self._variation_data = {}
        else:
            self._variation_data = variation_data
        self._reaction = reaction
        self._sample = sample
        self._props = None
        self._segments = None

    @property
    def gas_phase_data(self) -> GasPhaseObj:
        if not isinstance(self._props.get('gas_phase_data'), GasPhaseObj):
            gas_phase_data = self._sample._properties.get('gas_phase_data').copy_with_sample(
                self)
            gas_phase_data.set_time(**self._variation_data.get('duration', {'value': gas_phase_data.time_in_h}))
            gas_phase_data.set_temperature(
                **self._variation_data.get('temperature', {'value': gas_phase_data.temperature_in_k}))
            gas_phase_data.ppm = self._variation_data.get('concentration', {'value': gas_phase_data.ppm})[
                'value']
            self._props['gas_phase_data'] = gas_phase_data
        return self._props['gas_phase_data']

    def _extract_amount(self):
        self._props = {}
        role = self._sample.role_in_reaction
        amount_key = 'real_amount' if role == 'products' else 'target_amount'
        if role == 'products':
            self._props[amount_key] = UnitDict(**self._variation_data.get('mass', self._sample.get_amount()))
            if self._sample.gas_type == GasType.GAS:
                self._props['gas_phase_data'] = self.gas_phase_data
            self._props['equivalent'] = self._variation_data.get('yield', {}).get('value')
        else:
            if self._is_solvent:
                self._props[amount_key] = UnitDict(**self._variation_data.get('volume', self._sample.get_amount()))
            else:
                self._props[amount_key] = UnitDict(**self._variation_data.get('amount', self._sample.get_amount()))
                self._props['equivalent'] = self._variation_data.get('equivalent', {}).get('value')
        if self._props.get('equivalent') is None:
            self._props['equivalent'] = self._sample.equivalent

    @property
    def sample(self) -> Sample:
        return self._sample

    @property
    def _properties(self) -> dict:
        variation_keys = ["target_amount", "real_amount", "equivalent", "gas_phase_data"]
        if self._props is None:
            self._extract_amount()

        self._props |= {k: v for k, v in self._sample._properties.items() if k not in variation_keys}
        return self._props

    @_properties.setter
    def _properties(self, props: dict):
        pass

    def clean(self):
        self.update_equivalent()
        role = self.role_in_reaction
        amount_data = {}
        if role == 'products':
            amount_data['yield'] = {'value': self.equivalent, 'unit': None}
        elif role != 'solvents':
            amount_data['equivalent'] = {'value': self.equivalent, 'unit': None}
        if self.gas_type == GasType.GAS:
            amount_data['duration'] = {'value': convert_value(self.gas_phase_data.time_in_h, 'h', 's'),
                                       'unit': 'Second(s)'}
            amount_data['temperature'] = {'value': convert_value(self.gas_phase_data.temperature_in_k, 'K', '°C'),
                                          'unit': '°C'}
            amount_data['concentration'] = {'value': self.gas_phase_data.ppm, 'unit': 'ppm'}
            amount_data['turnoverFrequency'] = {'value': self.ton_per_h, 'unit': None}
            amount_data['turnoverNumber'] = {'value': self.ton, 'unit': None}
        if role != 'solvents':
            amount_data['mass'] = {'value': self.gram, 'unit': 'g'}
            amount_data['amount'] = {'value': self.mol, 'unit': 'mol'}
        amount_data['volume'] = {'value': self.liter, 'unit': 'l'}
        for key, value in amount_data.items():
            if amount_data[key]['value'] is None or isnan(amount_data[key]['value']):
                amount_data[key]['value'] = 0

        aux = self._variation_data.get('aux', {})
        return amount_data | {
            'aux': {
                "coefficient": self.properties['coefficient'],
                "isReference": self.properties['reference'],
                "loading": aux.get('loading'),
                "purity": self.properties['purity'],
                "density": self.properties['density'],
                "molarity": self.properties['molarity']['value'],
                "molecularWeight": self.molecule['molecular_weight'],
                "sumFormula": self.molecule['sum_formular'],
                "gasType": self.gas_type.value,
                "vesselVolume": self.vessel_size,
                "materialType": SampleVariationType.from_role_name(role).value
            }
        }

    def save(self, *args, **kwargs):
        raise NotImplementedError(f'This sample is only a Variation of {self.short_label} and cannot be saved!')



class SegmentVariation(Segment):
    allowed_fields = [FieldType.INTEGER, FieldType.TEXT, FieldType.SELECT, FieldType.SYSTEM_DEFINED]

    def __init__(self, generic_segment: dict, segment_data: Optional[dict], variation_data: list):
        super().__init__(generic_segment, segment_data)
        if segment_data is None:
            self.load()
        for values in variation_data:
            ln, fn = self._validator.convert_keys_to_labels(values['layer'], values['field'])
            self.layer[ln][fn] = values['value']

        for layer_label, layer_value in {**self.layer}.items():
            for field_label, field_value in {**layer_value}.items():
                if not self._validator.field_type(layer_label, field_label) in self.allowed_fields:
                    del self.layer.data[layer_label][field_label]
            if len(self.layer[layer_label]) == 0:
                del self.layer.data[layer_label]

    def clean(self):
        values = {}

        for layer_label, layer_value in self.layer.items():
            for field_label, field_value in layer_value.items():
                if self._validator.field_type(layer_label, field_label) in self.allowed_fields:
                    lk, fk = self._validator.convert_labels_to_keys(layer_label, field_label)
                    if isinstance(field_value, (PropertyDict, dict)):
                        field_value = field_value['value']
                    values[f'{self._generic_segment['label']}___{lk}___{fk}'] = {'value': field_value}
        return values


class SegmentsVariation(Segments):

    def __init__(self, generic_segments: GenericSegments, element_type: str, segments_json: list[dict],
                 variation_json: dict):
        if segments_json is None:
            segments_json = []
        if variation_json is None:
            self._variation_json = {}
        else:
            self._variation_json = variation_json
        super().__init__(generic_segments, element_type, segments_json)

    def _populate_segments(self, segments_json):
        for seg in self._all_seg_classes:
            variation_json = []
            seg_label = seg.get('label')
            for k, x in self._variation_json.items():
                [segment, layer, field] = k.split('___')
                if segment == seg_label:
                    variation_json.append({'layer': layer, 'field': field, 'value': x})
            self.data[seg_label] = SegmentVariation(seg,
                                                    next((x for x in segments_json if
                                                          x.get('segment_klass_id') == seg.get('id')),
                                                         None),
                                                    variation_json)
    def clean(self):
        cleaned_value = {}
        for segment in self.data.values():
            if isinstance(segment, SegmentVariation):
                cleaned_value |= segment.clean()
        return cleaned_value


class Variation(Reaction):
    def __init__(self, reaction: Reaction, variation_data: dict):
        params = reaction.copy_params()
        params['avoid_load'] = True
        super().__init__(**params)
        self._reaction = reaction
        self.id = -1
        self._variation_data = variation_data
        self._materials = {}
        self._props = None
        self.populate()
        self._segments = None

    def populate(self):
        self.id = self._variation_data['id']
        for mat_type_name in ['starting_materials', 'reactants', 'products', 'solvents']:
            mat_type = SampleVariationType.from_role_name(mat_type_name)
            self._materials[mat_type] = [
                self.sample_variation_factory(x, mat_type) for x in
                getattr(self._reaction, mat_type_name)]

    @property
    def segments(self) -> Optional[Segments]:

        if self._segments is None:
            segment_variation_data = self._variation_data.get('segmentData', {})
            segment_data = self.reaction.json_data.get('segments', [])

            self._segments = SegmentsVariation(self._generic_segments,
                                               self._reaction.element_type,
                                               segment_data,
                                               segment_variation_data)
        return self._segments

    def sample_variation_factory(self, sample: Sample, sample_type: SampleVariationType) -> SampleVariation:
        json_data = None
        for key, data in self._variation_data.get(sample_type.value, {}).items():
            if key == str(sample.id):
                json_data = data

        return SampleVariation(self, sample, json_data)

    def update_and_clean(self):
        return self.clean()

    def clean(self):
        for mat_type_name in ['starting_materials', 'reactants', 'products', 'solvents']:
            mat_type = SampleVariationType.from_role_name(mat_type_name)
            self._variation_data[mat_type.value] = {}
            for mat in self._materials[mat_type]:
                self._variation_data[mat_type.value][mat.id] = mat.clean()
        self._variation_data['segmentData'] = self.segments.clean()
        return self._variation_data

    @property
    def reaction(self) -> Reaction:
        return self._reaction

    @property
    def notes(self) -> str:
        return self._variation_data['metadata']['notes']

    @notes.setter
    def notes(self, value: str):
        self._variation_data['metadata']['notes'] = value

    @property
    def temperature_in_c(self) -> float:
        return convert_value(**self._variation_data['properties']['temperature'], out_unit='°C')

    @temperature_in_c.setter
    def temperature_in_c(self, value: float):
        self._variation_data['properties']['temperature']['value'] = value

    @property
    def reaction_properties(self):
        return self._variation_data['properties']

    def set_temperature(self, value, unit='°C'):
        self._variation_data['properties']['temperature']['value'] = convert_value(value, unit, '°C')

    @property
    def duration_in_s(self) -> float:
        return convert_value(**self._variation_data['properties']['duration'], out_unit='s')

    @duration_in_s.setter
    def duration_in_s(self, value: float):
        self._variation_data['properties']['duration']['value'] = value

    @property
    def variations(self):
        return []

    def set_duration(self, value, unit='s'):
        self._variation_data['properties']['duration']['value'] = convert_value(value, unit, 's')

    def link_analyses(self, analyses: Analyses):
        try:
            int(analyses.id)
            self._variation_data['metadata']['analyses'].append(analyses.id)
        except ValueError:
            raise ValueError("Analyses has no id. please save the Reaction first")

    def get_analyses(self) -> Iterator[Analyses]:
        for ana_id in self._variation_data['metadata']['analyses']:
            yield self._reaction._analyses.by_id(ana_id)

    @property
    def _properties(self) -> dict:
        variation_keys = ["starting_materials", "reactants", "products", "solvents"]
        if self._props is None:
            self._props = {k: getattr(self, k) for k in variation_keys}

        self._props |= {k: v for k, v in self._reaction._properties.items() if k not in variation_keys}
        return self._props

    @_properties.setter
    def _properties(self, props: dict):
        pass

    @property
    def starting_materials(self) -> list[SampleVariation]:
        return self._materials[SampleVariationType.STARTING_MATERIAL]

    @property
    def reactants(self) -> list[SampleVariation]:
        return self._materials[SampleVariationType.REACTANT]

    @property
    def products(self) -> list[SampleVariation]:
        return self._materials[SampleVariationType.PRODUCT]

    @property
    def solvents(self) -> list[SampleVariation]:
        return self._materials[SampleVariationType.SOLVENTS]


class Variations(MutableSequence):
    def __init__(self, reaction: 'Reaction'):
        # Initialize the list with given items
        self._data = list()
        self._reaction = reaction
        self._highest_id = 0
        self.populate(reaction.json_data['variations'])

    def populate(self, json_data: dict):
        for variation in json_data:
            v = Variation(self._reaction, variation)
            self.append(v)
            self._highest_id = max(self._highest_id, variation['id'])

    def remove(self, value: Variation) -> bool:
        try:
            idx = next(idx for idx, v in enumerate(self) if v.id == value.id)
            self.pop(idx)
        except StopIteration:
            return False
        return True

    def add_new(self) -> Variation:
        self._highest_id += 1
        variation = self.empty_variation(self._highest_id)
        v = Variation(self._reaction, variation)
        self.append(v)
        return v

    @classmethod
    def empty_variation(cls, highest_id: int) -> dict:
        return {
            "id": highest_id,
            "properties": {
                "temperature": {
                    "value": 0,
                    "unit": "°C"
                },
                "duration": {
                    "value": 0,
                    "unit": "Second(s)"
                }
            },
            "metadata": {
                "notes": "",
                "analyses": []
            },
            "reactants": {},
            "products": {},
            "solvents": {},
            "startingMaterials": {}
        }

    def sort(self):
        self._data = sorted(self._data, key=lambda v: v.id)

    def clean(self):
        return [variation.update_and_clean() for variation in self._data]

    def _prepare_variation(self, json_data: dict):
        empty_variation = self.empty_variation(self._highest_id)
        return merge_dicts(empty_variation, json_data)

    def __getitem__(self, index):
        # Retrieve the item at the given index
        return self._data[index]

    def __setitem__(self, index, value):
        # Set the item at the given index
        self._data[index] = value
        self.sort()

    def __delitem__(self, index):
        # Delete the item at the given index
        del self._data[index]

    def insert(self, index, value):
        # Insert an item at the given index
        self._data.insert(index, value)
        self.sort()

    def __len__(self):
        # Return the length of the list
        return len(self._data)

    def __repr__(self):
        # Return a string representation of the list
        return f"{repr(self._data)}"
