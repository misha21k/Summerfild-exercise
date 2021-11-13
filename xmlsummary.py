import optparse
import os
import queue
import threading
from xml import sax
import Util


class Worker(threading.Thread):

    def __init__(self, work_queue, results_queue, number):
        super().__init__()
        self.work_queue = work_queue
        self.results_queue = results_queue
        self.number = number

    def run(self):
        while True:
            try:
                name = self.work_queue.get()
                self.process(name)
            finally:
                self.work_queue.task_done()

    def process(self, filename):
        tags = set()
        try:
            handler = TagSaxHandler(tags)
            sax.parse(filename, handler)
            if tags:
                result = f'{self.number}{filename} is an XML file that uses the following tags:'
                for tag in tags:
                    result += f'\n\t{tag}'
                self.results_queue.put(result)
            else:
                self.results_queue.put(f"{self.number}{filename} is an XML file that don't use tags")
        except (EnvironmentError, sax.SAXParseException) as err:
            self.results_queue.put(f'{self.number}{filename} is an XML file that has the following error:\n'
                                   f'\t{err}')


class TagSaxHandler(sax.handler.ContentHandler):

    def __init__(self, tags):
        super().__init__()
        self.__tags = tags

    def startElement(self, name, attrs):
        self.__tags.add(name)


def main():
    opts, path = parse_options()

    if opts.verbose:
        print("Creating {0} thread{1}...".format(
              opts.count, Util.s(opts.count)))
    work_queue = queue.Queue()
    results_queue = queue.Queue()
    for i in range(opts.count):
        number = "{0}: ".format(i + 1) if opts.debug else ""
        worker = Worker(work_queue, results_queue, number)
        worker.daemon = True
        worker.start()

    results_thread = threading.Thread(target=lambda: print_results(results_queue))
    results_thread.daemon = True
    results_thread.start()

    if opts.verbose:
        print("Creating file list...")
    for root, dirs, files in os.walk(path):
        for filename in files:
            fullname = os.path.join(root, filename)
            try:
                with open(fullname, "rb") as f:
                    if f.read(5) == b'<?xml':
                        work_queue.put(fullname)
            except EnvironmentError:
                continue

    work_queue.join()
    results_queue.join()


def print_results(results_queue):
    while True:
        try:
            results = results_queue.get()
            if results:
                print(results)
        finally:
            results_queue.task_done()


def parse_options():
    parser = optparse.OptionParser(
            usage=("usage: %prog [options] [path]\n"
                   "outputs a summary of the XML files in path; path defaults to ."))
    parser.add_option("-t", "--threads", dest="count", default=7,
                      type="int",
                      help=("the number of threads to use (1..20) "
                      "[default %default]"))
    parser.add_option("-v", "--verbose", dest="verbose",
                      default=False, action="store_true")
    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true")
    opts, args = parser.parse_args()
    if not (1 <= opts.count <= 20):
        parser.error("thread count must be 1..20")
    return opts, args[0] if args else "."


main()
