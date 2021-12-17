from os import popen
from flask import Flask, flash, json, jsonify
from flask.helpers import url_for
from flask.wrappers import Response
import requests
mangadex_cover_url= "https://api.mangadex.org/cover"
mangadex_chapter_url = "https://api.mangadex.org/chapter"
mangadex_base_url= "https://api.mangadex.org/manga"
kitsu_bas_url= "https://kitsu.io/api/edge/manga"

def get_manga_by_name(title):
    
    url_cmd= f'{mangadex_base_url}?title="{title}"'
    print(url_cmd)
    responses = requests.get(url_cmd)
    responses = responses.json()
    results = False
    if responses['data']:
        results = {
            "search": title,
            "response": {}

    
        }
        tmp = {}

        for response in responses['data']:
            id = response['id']
            language= list(response['attributes']['title'].keys())
            api_title = response['attributes']['title'][language[0]]
            description = response['attributes']['description']['en']
            altTitles = response['attributes']['altTitles']
            result = {
                "id": id,
                "title": api_title,
                "altTitles": altTitles,
                "description": description,
                #"chapters": get_manga_chap() 
            }
            tmp[api_title] = result
        results['response'] = tmp

        return results
    else:
        flash('This manga doesnt exist or is not in the mangadex database', category='error')
        return results


def get_manga_by_id(id):
    url = mangadex_base_url + "/" + id
    response = requests.get(url)
    response = response.json()
    results = {
        'id_manga': id,
        'title': response['data']['attributes']['title']['en'],
        'description': response['data']['attributes']['description']['en'],
        'altTitles': response['data']['attributes']['altTitles']    }
    return results

def get_manga_chap(id):
    url = f'{mangadex_base_url}/{id}/aggregate'
    response = requests.get(url)
    response = response.json()
    chapters = response['volumes']['none']['chapters']
    # sorted_chap = [float(i) for i in list(response['volumes']['none']['chapters'].keys()) if i != 'none']
    # last_chap = max(sorted_chap)
    results= list()
    for i in chapters:
        chap = chapters.get(i)
        id_chap = chap['id']
        chap_nb = chap['chapter']
        url_chapter = f'{mangadex_chapter_url}/{id_chap}'

        response = requests.get(url_chapter)
        response = response.json()

        language = response['data']['attributes']['translatedLanguage']
        result = {
            'id' : id_chap,
            'chapter': chap_nb,
            'language': language
        }
        results.append({chap_nb: result})
    print(results)
    return results