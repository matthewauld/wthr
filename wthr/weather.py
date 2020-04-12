import requests
import atoma
import html
from collections import OrderedDict
en_to_fr = {
    'Current Conditions':'Conditions actuelles',
    'Warnings and Watches':'Veilles et avertissements',
    'Weather Forecasts':'Prévisions météo',
    'No watches or warnings in effect.': 'Aucune veille ou alerte en vigueur.',
    'Forecast':'Prévisions',
    'Current Conditions':'Conditions actuelles',
}


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class Weather:
    def __init__(self, city, province, lang, fancy = True):
        self.city = city
        self.lang = lang
        self.province = province
        self.link = "https://weather.gc.ca/rss/city/{}-{}_{}.xml".format(province,city,lang)
        self.label_style = color.BOLD
        self.alert_style = color.RED
        self.fancy = fancy

    def get_weather(self):
        r = requests.get(self.link)
        if r.status_code != 200:
            raise ValueError("request returned HTTP response of {}".format(r.status_code))

        feed = atoma.parse_atom_bytes(r.content)
        self.title = feed.title.value
        self.updated = feed.updated
        current_conditions = None
        self.forecast = OrderedDict()
        self.alerts = []
        for entry in feed.entries:
            if entry.categories[0].term == self.translate('Current Conditions'):
                if current_conditions is not None:
                    raise ValueError("There is more than one current conditions...")
                current_conditions = entry
            elif entry.categories[0].term == self.translate('Warnings and Watches'):
                if entry.summary.value == self.translate('No watches or warnings in effect.'):
                    self.has_alerts = False
                else:
                    self.has_alerts = True
                    self.alerts.append(entry)
            elif entry.categories[0].term == self.translate('Weather Forecasts'):
                e = entry.title.value.split(':')[0]
                self.forecast[e] = entry
            else:
                print("Error, unidentified category {}. Notify developer".format(entry.categories[0].term))
        self.current_conditions = {}

        self.current_summary = current_conditions.title.value

        current_conditions =  html.unescape(current_conditions.summary.value).split('<br/>\n')
        for entry in current_conditions:
            entry_elems = entry.split(':</b>')
            self.current_conditions[entry_elems[0][3:].strip()] = entry_elems[1].split('<br/>')[0].strip()


    def translate(self, value):
        if self.lang == 'e':
            return value
        else:
            return en_to_fr[value]


    def print_forecast(self):
        title_style = ""
        label_style = ""
        end_style = ""

        if self.fancy:
            label_style = self.label_style
            end_style = color.END
            title_style = self.label_style
        # print title
        self.print_title(self.translate("Forecast"),label_style)
        #print forecast
        for key,value in self.forecast.items():
            entry = value.title.value.split(":")
            print("{}{:20}:{}{}".format(label_style,entry[0],end_style,entry[1]))


    def print_title(self, title,style=''):
        end_style = ""
        if len(style)>0:
            end_style = color.END
        num_dashes = len(title)
        print("{}{}\n{}{}".format(style,title,'-'*num_dashes,end_style))


    def print_current_conditions(self):
        label_style = ""
        end_style = ""

        if self.fancy:
            label_style = self.label_style
            end_style = color.END
        self.print_title(self.translate("Current Conditions"),label_style)
        for key,value in self.current_conditions.items():
            print("{}{:20}:{} {}".format(label_style,key,end_style,value))

    def print_forecast_date(self,day):
        days = {
            'm':'Monday',
            't':"Tuesday",
            'th':'Thursday',
            'w':"Wednesday",
            'f':"Friday",
            's':"Saturday",
            'su':"Sunday"
        }

        for key,value in self.forecast.items():
            if days[day] in key:
                print(value.title.value)

    def print_alerts(self):
        label_style = ""
        content_style = ""
        end_style = ""

        if self.fancy:
            title_style = self.label_style + self.alert_style
            content_style = self.alert_style
            end_style = color.END

        if self.has_alerts:
            for alert in self.alerts:
                self.print_title(alert.title.value,title_style)
                print("{}{}{}\n".format(content_style,alert.summary.value,end_style))
