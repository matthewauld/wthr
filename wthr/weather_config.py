import yaml


class WthrConfig:
    provinces = ['on','ab','mb','sk','bc','qc','nb','ns','pe','nl','nt','yt','nu']
    default_yaml = '''#wthr configuration file
#Default Weather
#---------------
language: {language}
province: {province}
region_id: {region_id}
'''
    def __init__(self):
        self.language    = None
        self.province    = None
        self.region_id   = None


    def load(self,path):
        with open(path,'r') as f:
                options = yaml.safe_load(f)
                if 'language' in options:
                    self.language  = options['language']
                if 'province' in options:
                    # 'on' is interpreted as True by pyyaml... so we fix that
                    if options['province'] is True:
                        self.province = 'on'
                    else:
                        self.province  = options['province']
                if 'region_id' in options:
                    self.region_id  = options['region_id']

    def get_user_config(self, path, **kwargs):
        if 'language' not in kwargs:
            while True:
                print("Enter preferred langauge(en,fr)")
                i = input('>')
                if 'e' in i.lower():
                    self.language = 'en'
                    break
                if 'f' in i.lower():
                    self.language = 'fr'
                    break
                print("Invalid entry.")
        else:
            self.language = kwargs['langauge']

        if 'province' not in kwargs:
            while True:
                print("Enter province you are in:")
                i = input('>')
                for prov in self.provinces:
                    if prov in i.lower():
                        self.province = prov
                        break
                if self.province is not None:
                    break
                print("Invalid entry.")
                print("please enter one of {}".format(', '.join(self.provinces)))
        else:
            self.province = kwargs['province']
        if 'region_id' not in kwargs:
            while True:
                print("Enter your region_id:")
                i = input('>')
                try:
                    int(i)
                    self.region_id = i
                    break
                except:
                    pass
                print("Invalid entry.")
        else:
            self.region_id = kwargs['region_id']
        yaml_file = self.default_yaml.format(language=self.language, province=self.province, region_id=self.region_id)
        with open(path, 'w') as f:
            f.write(yaml_file)
