import sys
from pymarc import MARCReader

DEBUG_ON_IMPORT_SAVE_ERROR = False

def multifile_iter_records(files):
    for f in files:
        if not hasattr(f, 'read'):
            f = open(f)
        reader = MARCReader(f, to_unicode=True)
        for record in reader:
            yield record

class BaseHandler(object):
    """
    In subclasses, define 
    
    pre_harvest
    
    a clean(record), which is called with each marc record and returns a dictionary of parameters that could be sent to a model save().
    
    post_harvest
    """

    @staticmethod
    def get_separated_subfields(record, tag, subfields, separator=" "):
        results = []
        for field in record.get_fields(tag):            
            parts = []
            for s in subfields:
                part = field[s]
                if part:
                    parts.append(part.strip())
        
            results.append(separator.join(parts).replace(" :", ":").replace(" ;", ";"))
        return results
    
    @staticmethod
    def get_formatted_fields(record, tag):
        return [field.format_field() for field in record.get_fields(tag)]    
    
    def __init__(self, model, pk="id"):
        self.model = model
        self.pk = pk
    
    def process(self, files, post_only=False):
        if not post_only:
            self.pre_harvest()
            #this steps through given files, and calls hadle_elem after the end of each element.
            fails = 0
            count = 0

            for record in multifile_iter_records(files):
                # try:
                    d = self.clean(record)
                    if d is not None:
                        try: #update (deleting from a RDBMS updates FK)
                            q = { self.pk: d[self.pk] }
                            m = self.model.objects.get(**q)
                            del d[self.pk]
                            for k,v in d.items():
                                setattr(m, k, v)
                            m.save()             
                        except self.model.DoesNotExist:
                            m = self.model(**d)
                            m.save()
                        count += 1
                        if count % 100 == 0:
                            print "saved %s items" % count
                    else: #d is none (fail)
                        fails += 1
                        if fails % 10 == 0:
                            print "SKIPPED %s items" % fails               
                # except Exception as e:
                #     if DEBUG_ON_IMPORT_SAVE_ERROR:
                #         from pprint import pprint
                #         pprint(record)
                #         print "Cleaned data:"
                #         pprint(d)
                #         pprint(e)
                #         import pdb; pdb.set_trace()
                #     else:
                #         raise e
                        
        self.post_harvest()
        
    
    def pre_harvest(self):
        pass
    
    def clean(self, record):
        return None
        
    def post_harvest(self):
        pass