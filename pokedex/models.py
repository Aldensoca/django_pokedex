from django.db import models

class type(models.Model):
    type = models.CharField(max_length=16, primary_key=True, unique=True)
    color = models.CharField(null=True)
    def __str__(self):
      return self.type

class pokemon(models.Model):
    pkmn_id = models.IntegerField(unique=True, primary_key=True)
    pkmn_name = models.CharField(max_length=32,unique=True)
    pkmn_height = models.IntegerField()
    pkmn_weight = models.IntegerField()
    pkmn_type1 = models.ForeignKey(type, on_delete=models.SET_NULL, null=True, related_name='type1')
    pkmn_type2 = models.ForeignKey(type, on_delete=models.SET_NULL, null=True, blank=True, related_name='type2')
    pkmn_desc = models.CharField(max_length=255)
    
    def __str__(self):
        rtn = f'{self.pkmn_id:04} | {self.pkmn_name}'
        return rtn
        

#class trainer(models.Model):
#    trainer_id = models.IntegerField(max_length=999999)
#    trainer_name = models.models.CharField(max_length=16)