from collections import defaultdict

import numpy as np
import pandas as pd

from Supplychain.Protocol.protocol import AbstractParameterTransformation


class DefaultTransformation(AbstractParameterTransformation):
    """
    A class used to generate and store the transformation applied to the generic algorithm output

    We need a list of decision variables which allows us to transform an array of float to a map of datapath to values
    """

    class BasicTransform(object):
        """
        Define a basic transformation of the data using :
        - a starting index
        - a size of the data to use
        - a list of entities
        - an index in the final array
        """
        index = None
        size = None
        entities = None
        end_index = None
        schedule = None

        def __init__(self, index, size, entities, end_index=0, schedule=False):
            self.index = index
            self.size = size
            self.entities = entities
            self.end_index = end_index
            self.schedule = schedule

        def transform(self, d):
            """

            :param d: the entrance datas
            :return: the transformed datas
            """
            pass

        def __str__(self):
            return str(self.index) + " - " + str(self.size) + " - " + str(self.end_index) + " : " + str(self.entities)

    class InverseTransform(BasicTransform):
        """
        A specialisation of BasicTransform used to generate inverted data
        """

        def transform(self, data):
            """
            For the first entity we keep the original data and for the second we return the inverse of the data
            :param data: an array of data
            :return: an array of tuple : entity, transformed data
            """
            return [(self.entities[0], data[self.index: self.index + self.size]),
                    (self.entities[1], 1 - data[self.index: self.index + self.size])]

    class NormalisationTransform(BasicTransform):
        """
        A specialisation of BasicTransform used to normalize data
        """

        def transform(self, data):
            """
            For each cycle we normalize the data before distributing it to each entity
            :param data: an array of data
            :return: an array of tuple : entity, transformed data
            """
            n_entities = len(self.entities)
            tmp = data[self.index: self.index + self.size * n_entities].reshape((self.size, n_entities))
            tmp = list((tmp / np.linalg.norm(tmp, axis=1, ord=1)[:, None]).T)
            return zip(self.entities, tmp)

    class NoTransform(BasicTransform):
        """
        A specialisation of Basic transform that map the data for the entity without transformations
        """

        def transform(self, data):
            return [(self.entities[0], data[self.index: self.index + self.size]), ]

    transformation_template = None
    start_cycle = None
    array_size = None
    steps_per_cycle = None

    @staticmethod
    def rowToKey(row):
        """
        :param row: an entry of the decision_variable.csv
        :return: a tuple (datapath , <optional> subentity)
        """
        entity_name = row['Entity']
        attribute_name = row['Attribute']
        if attribute_name is None:
            return None
        entity_key = f"Model::{{Entity}}IndustrialNetwork::{{Entity}}{entity_name}"
        attribute_key = f"::@{attribute_name}"
        if row['Type'] == 'Machine':
            sub_entity_name = row['Operation']
            return f"{entity_key}::{{Entity}}{sub_entity_name}{attribute_key}",
        return f"{entity_key}{attribute_key}",

    def __init__(self, dv_df, machines, total_cycles, steps_per_cycle):
        """
        We initialize the transformation using the decision variables
        :param dv_df: A pandas DF using decision_variable.csv
        """
        self.transformation_template = list()
        index = 0
        self.start_cycle = 0
        self.array_size = total_cycles
        self.steps_per_cycle = steps_per_cycle

        if not dv_df.empty:
            nb_group = max(list(dv_df['Group'])) + 1
            # Loop on the different groups
            for group in range(nb_group):
                temp = dv_df[dv_df['Group'] == group]
                temp.index = pd.RangeIndex(len(temp.index))

                cycles = temp['EndCycle'][0] - temp['StartCycle'][0] + 1
                final_index = temp['StartCycle'][0] - self.start_cycle
                entries = []
                for _, row in temp.iterrows():
                    entries.append(self.rowToKey(row))

                nb_entries = len(entries)
                if nb_entries == 2:
                    self.transformation_template.append(self.InverseTransform(index=index,
                                                                              size=cycles,
                                                                              entities=entries,
                                                                              end_index=final_index))
                    index += cycles
                else:
                    self.transformation_template.append(self.NormalisationTransform(index=index,
                                                                                    size=cycles,
                                                                                    entities=entries,
                                                                                    end_index=final_index))
                    index += cycles * nb_entries
        for machine in machines:
            machine_data_path = ("Model::{Entity}IndustrialNetwork::{Entity}" + machine + "::@OpeningRateSchedule",)
            self.transformation_template.append(self.NoTransform(index=index,
                                                                 size=total_cycles,
                                                                 entities=[machine_data_path, ],
                                                                 end_index=0,
                                                                 schedule=True))
            index += total_cycles

    def list_to_schedule(self, values):
        return {
            str(i * self.steps_per_cycle): v
            for i, v in enumerate(values)
        }

    def applies(self, _data, _seed=0):
        """
        We apply the tranformation on the data
        :param _data: an array of data
        :param _seed: an int used as the seed for the simulation
        :return: a dict ready to be given to the simulation
        """
        data = np.array(_data)
        ret_dict = defaultdict(list)
        if _seed > 0:
            ret_dict["{Model}Model::{Attribute}Seed"] = _seed

        for t in self.transformation_template:
            index = t.end_index
            padding = t.size
            for a, b in t.transform(data):
                if a is None:
                    # Non used DVs have entity names set to None
                    continue
                entity = a[0]
                if len(a) == 1:
                    if not len(ret_dict[entity]):
                        ret_dict[entity] = [0] * self.array_size
                    ret_dict[entity][index:index + padding] = b
                    if t.schedule:
                        ret_dict[entity] = self.list_to_schedule(ret_dict[entity])
                else:
                    subentity = a[1]
                    # Array is empty
                    if not len(ret_dict[entity]):
                        for i in range(self.array_size):
                            ret_dict[entity].append({subentity: 0})
                    # subentity is not in the array
                    if subentity not in ret_dict[entity][0]:
                        for i in range(self.array_size):
                            ret_dict[entity][i][subentity] = 0
                    # Set values from transformation to array
                    for i in range(len(b)):
                        ret_dict[entity][index + i][subentity] = b[i]
        # We apply a transformation to str on all the values
        return {k: str(ret_dict[k]).replace("'", "\"") for k in ret_dict}
