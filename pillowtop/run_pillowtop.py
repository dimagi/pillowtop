from restkit.session import set_session; set_session("gevent")
from pillowtop import get_all_pillows
from multiprocessing import Pool


def run_pillow(pillow_class):
    try:
        pillow_class.run()
    except Exception, ex:
        print "Some pillow error: %s: %s" % (pillow_class.__class__.__name__, ex)


#standalone pillowtop runner
def start_pillows():
    #gevent patching: logging doesn't seem to work unless thread is not patched

    pillows = get_all_pillows()
    p = Pool(len(pillows))
    try:
        while True:
            p.map(run_pillow, pillows)
            print dir(p)
            print p
            p.close()
            p.join()
            print "Pillows all joined and completed - restarting again"
            #this shouldn't happen
    except KeyboardInterrupt, e:
        print 'parent received control-c'
        pass

if __name__ == "__main__":
    start_pillows()

