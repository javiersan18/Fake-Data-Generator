import numpy
import random
import datetime
from generator.templates.data_template import DataTemplate
from tzlocal import get_localzone
local = get_localzone()


class ApacheLogsTemplate(DataTemplate):

    def __init__(self, type="ELF"):
        self.type = type
        super().__init__(self)

    def generate(self):

        otime = datetime.datetime.now()

        http_response = ['200', '404', '500', '301']
        http_verb = ['GET', 'POST', 'DELETE', 'PUT']
        endpoints = ['/clients', '/farms', '/containers', '/routes', '/installations', '/incidences']
        ualist = [self.faker.firefox, self.faker.chrome, self.faker.safari, self.faker.internet_explorer, self.faker.opera]

        ip = self.faker.ipv4()
        dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
        tz = datetime.datetime.now(local).strftime('%z')
        vrb = numpy.random.choice(http_verb, p=[0.6, 0.1, 0.1, 0.2])

        uri = random.choice(endpoints)

        resp = numpy.random.choice(http_response, p=[0.9, 0.04, 0.02, 0.04])
        byt = int(random.gauss(5000, 50))
        referer = self.faker.uri()
        useragent = numpy.random.choice(ualist, p=[0.5, 0.3, 0.1, 0.05, 0.05])()

        if self.type == 'CLF':
            return ('%s - - [%s %s] "%s %s HTTP/1.0" %s %s\n' % (ip, dt, tz, vrb, uri, resp, byt))
        elif self.type == 'ELF':
            return ('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (
                ip, dt, tz, vrb, uri, resp, byt, referer, useragent))
