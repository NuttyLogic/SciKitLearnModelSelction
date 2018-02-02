#! /usr/bin/env python3

import pickle
import subprocess


class LaunchOptimizationJob:

    def __init__(self, dictionary_tuple='tupple of dicts', model_interface='model to optimize', sge_cores=8, sge_mem=2,
                 sge_time=8, simultaneous_jobs=20, optimization_batch_name='batch_name',
                 optimization_batch_directory='path',
                 sge_output_folder='', sge_user=''):
        self.dictionaries = dictionary_tuple
        self.model_interface = model_interface
        self.sge_cores = sge_cores
        self.sge_mem = sge_mem
        self.sge_time = sge_time
        self.jobs = simultaneous_jobs
        self.batch_name = optimization_batch_name
        self.batch_directory = optimization_batch_directory
        self.batch_path = '%s%s' % (self.batch_directory, self.batch_name)
        self.batch_input = '%s.batch_input' % self.batch_path
        self.sge_output = sge_output_folder
        self.sge_user = sge_user
        self.batch_length = 0

    def set_sample_list(self):
        out = open(self.batch_input, 'w')
        for model in self.dictionaries:
            self.batch_length += 1
            assert isinstance(model, dict)
            model_name = model['output_name']
            model_input_args = '%s%s.input_arguments' % (self.batch_directory, model_name)
            pickle.dump(model, open(model_input_args, 'wb'))
            out.write('%s\n' % model_input_args)
        out.close()

    def set_output_shell(self):
        out = open('%s.sh' % self.batch_path, 'w')
        out.write('# !/bin/bash\n')
        out.write('# $ -pe shared %s\n' % str(self.sge_cores))
        out.write('# $ -l h_rt=%s:00:00\n' % str(self.sge_time))
        out.write('# $ -l h_data==%sG\n' % str(self.sge_mem))
        out.write('# $ -o %s\n' % self.sge_output)
        out.write('# $ -e %s\n' % self.sge_output)
        out.write('# $ -M %s\n' % self.sge_user)
        out.write('# $ -m a\n')
        out.write('while getopts d: option\n')
        out.write('do\n')
        out.write(' case "${option}"\n')
        out.write(' in\n')
        out.write(' D) input_dictionary_list=${OPTARG};;\n')
        out.write(' esac\n')
        out.write('done\n')
        out.write('. /u/local/Modules/default/init/modules.sh\n')
        out.write('module load python/3.6.1\n')
        out.write('sample_name=$(cat $input_dictionary_list | head -${SGE_TASK_ID} | tail -1 )\n')
        out.write('python3 %s -i $sample_name\n' % self.model_interface)
        out.close()

    def submit_batch_job(self):
        batch_array_size = '1-%s' % str(self.batch_length)
        qsub_command = ['qsub', '-M', self.sge_user, '-m', 'a', '-t', batch_array_size, '-tc', str(self.jobs),
                        '%s.sh' % self.batch_path, '-d', self.batch_input]
        subprocess.run(qsub_command)




