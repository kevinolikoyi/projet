from threading import Thread, Condition
import time
import random
import queue
import sched, time
le_timer = sched.scheduler(time.time, time.sleep)
condition = Condition()

memoire_partage=int(input("Entrer la taille de la memoire: "))
producteur=int(input("Entrer le nombre de producteur: "))
consommateur=int(input("Entrer le nombre de consommateur: "))
les_producteurs=0
les_consommateurs=0
queue = queue.Queue(10)
la_queue = []


class ProducerThread(Thread):
    def run(self):
        nums = range(9)
        global queue
        global la_queue
        while True:
            def faire_production(sc):
                condition.acquire()
                if len(la_queue) == memoire_partage:
                    condition.wait()
                else:
                    num = random.choice(nums)
                    la_queue.append(num)
                    queue.put(num)
                condition.notify()
                condition.release()
                time.sleep(random.random())


                le_timer.enter(2, 1, faire_production, (sc,))
            le_timer.enter(2, 1, faire_production, (le_timer,))
            le_timer.run()
            

class ConsumerThread(Thread):
    def run(self):
        global queue
        global la_queue
        while True:
            def faire_consommation(sc):
                condition.acquire()
                if not la_queue:
                    condition.wait()
                
                num = queue.get()
                num= la_queue.pop(0)
                queue.task_done()
                condition.notify()
                condition.release()
                time.sleep(random.random())
                le_timer.enter(6, 1, faire_consommation, (sc,))
            le_timer.enter(6, 1, faire_consommation, (le_timer,))
            le_timer.run()

while les_producteurs<producteur:
    ProducerThread().start()
    les_producteurs=les_producteurs + 1

while les_consommateurs<consommateur:
    ConsumerThread().start()
    les_consommateurs=les_consommateurs + 1

def affiche_queue(sc): 
    global la_queue

    print(la_queue)
    le_timer.enter(1, 1, affiche_queue, (sc,))
le_timer.enter(1, 1, affiche_queue, (le_timer,))
le_timer.run()