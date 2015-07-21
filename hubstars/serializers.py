import re

from rest_framework import serializers

import requests

url_regex = "https:\/\/github\.com\/(\S+)\/(\S+)"

class BattleSerializers (serializers.Serializer):
  url1 = serializers.RegexField(url_regex, label="URL 1")
  url2 = serializers.RegexField(url_regex, label="URL 2")
  
  def validate_url (self, value, field):
    regex = re.search(url_regex, value)
    user = regex.group(1)
    repo = regex.group(2)
    
    try:
      response = requests.get(
        'https://api.github.com/repos/{}/{}'.format(user, repo))
        
    except:
      raise serializers.ValidationError("Github Not Responding")
      
    else:
      if response.status_code == 200:
        setattr(self, 'json{}'.format(field), response.json())
        
      elif response.status_code == 404:
        raise serializers.ValidationError("Repo Not Found")
        
      elif response.status_code == 403:
        raise serializers.ValidationError("Github API Rate Limited")
        
      else:
        print response.status_code
        print response.json()
        raise serializers.ValidationError("Error getting Repo")
        
      return value
      
  def validate_url1 (self, value):
    return self.validate_url(value, 1)
    
  def validate_url2 (self, value):
    return self.validate_url(value, 2)
    
  def battle_data (self):
    winner = None
    if self.json1['stargazers_count'] > self.json2['stargazers_count']:
      winner = self.json1['full_name']
      
    elif self.json1['stargazers_count'] < self.json2['stargazers_count']:
      winner = self.json2['full_name']
      
    return {
      'project1': self.compile_json(self.json1),
      'project2': self.compile_json(self.json2),
      'winner': winner,
    }
    
  def compile_json (self, json):
    return {
      'name': json['full_name'],
      'stars': json['stargazers_count'],
      'forks': json['forks_count'],
      'watchers': json['watchers_count'],
    }
    