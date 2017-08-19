# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

def return_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    return np.true_divide(np.sum(minima), np.sum(hist_2))


def main_aula():
    image = plt.imread('hulk.png')
    hr,bins = np.histogram(image[:,:,0], bins=256)
    hg,bins = np.histogram(image[:,:,1], bins=256)
    hb,bins = np.histogram(image[:,:,2], bins=256)
#    plt.plot(hr, color='r')
#    plt.plot(hg, color='g')
#    plt.plot(hb, color='b')
    
    image2 = plt.imread('maravilha.png')
    
    hr2,bins = np.histogram(image2[:,:,0], bins=256)
    hg2,bins = np.histogram(image2[:,:,1], bins=256)
    hb2,bins = np.histogram(image2[:,:,2], bins=256)
#    plt.plot(hr2, color='r')
#    plt.plot(hg2, color='g')
#    plt.plot(hb2, color='b')
    
    # comparando com ele mesmo
    r = return_intersection(hr, hr)
    g = return_intersection(hg, hg)
    b = return_intersection(hb, hb)
#    compatibilidade = r + g + b # resulta em 3 que é o máximo
    
    r2 = return_intersection(hr, hr2)
    g2 = return_intersection(hg, hg2)
    b2 = return_intersection(hb, hb2)
    compatibilidade = r2 + g2 + b2
    print(compatibilidade)
    

    
    return 0

def main_tarefa():
    
    images = [
        { 'name': 'America', 'image': plt.imread('America.png') },
        { 'name': 'Batman', 'image': plt.imread('Batman.png') },
        { 'name': 'Ferro', 'image': plt.imread('Ferro.png') },
        { 'name': 'Flash', 'image': plt.imread('Flash.png') },
        { 'name': 'Hulk', 'image': plt.imread('Hulk.png') },
        { 'name': 'Maravilha', 'image': plt.imread('Maravilha.png') },
        { 'name': 'Super', 'image': plt.imread('super.png') },
        { 'name': 'Wolverine', 'image': plt.imread('wolverine.png') }
    ]
    
    quem = [
        plt.imread('QUEM1.png'),
        plt.imread('QUEM2.png'),
        plt.imread('QUEM3.png'),
        plt.imread('QUEM4.png'),
        plt.imread('QUEM5.png')
    ]
    
    results = []
    
    for j in range(len(quem)):
        q_img = quem[j]
        results.append([])
        hr_quem, bins = np.histogram(q_img[:, :, 0], bins=256)
        hg_quem, bins = np.histogram(q_img[:, :, 1], bins=256)
        hb_quem, bins = np.histogram(q_img[:, :, 2], bins=256)
        for i in images:
            hr, bins = np.histogram(i['image'][:, :, 0], bins=256)
            hg, bins = np.histogram(i['image'][:, :, 1], bins=256)
            hb, bins = np.histogram(i['image'][:, :, 2], bins=256)
            ihr = return_intersection(hr, hr_quem)
            ihg = return_intersection(hg, hg_quem)
            ihb = return_intersection(hb, hb_quem)
            results[j].append(ihr + ihg + ihb)
            
    for i_quem in range(len(results)):
        q = results[i_quem]
        maior = 0
        i = 0
        for j_result in range(len(q)):
            if (q[j_result] > maior):
                maior = q[j_result]
                i = j_result
        print('QUEM ' + str(i_quem+1) + ' é ' + images[i]['name'])
            
    # plt.barh(range(len(results1)), results1, 0.5, color='red')
    
    
    return 0

if __name__ == '__main__':
    main_tarefa()