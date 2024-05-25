from django.db import models

# Create your models here.

class haplotype(models.Model):
    mosaicID = models.CharField(max_length=255)  # varchar 类型对应 Django 的 CharField
    geneID = models.CharField(max_length=255)
    areaType = models.CharField(max_length=255)
    length = models.IntegerField()  # int 类型对应 Django 的 IntegerField
    nucleotideSequence = models.TextField()  # longtext 类型对应 Django 的 TextField
    id = models.AutoField(primary_key=True) # 建议创建数据表时设置一个行号为主键，否则 Django 会自动创建一个自增的主键字段 haplotype.id
    class Meta:
        db_table = 'haplotype' # 指定Django模型映射到的数据库表名, 默认是 app名_模型名
        managed = False  # 如果为False，Django将不会在数据库中创建表或删除表

    def __str__(self):
        return f"{self.mosaicID}"  # 用于返回模型的字符串表示，例如在admin界面显示
    
class snp(models.Model):
    mosaicID = models.CharField(max_length=255)
    areaType = models.CharField(max_length=255)
    SNPSite = models.IntegerField()
    SNPType = models.CharField(max_length=255)
    IsoSeqEvidence = models.CharField(max_length=255)
    RNASeqEvidence = models.CharField(max_length=255)
    haplotypeSNP = models.TextField()
    color = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'snp'
        managed = False

    def __str__(self):
        return f"{self.mosaicID}"  # 用于返回模型的字符串表示，例如在admin界面显示
    
class transcript(models.Model):
    mosaicID = models.CharField(max_length=255)
    geneID = models.CharField(max_length=255)
    transcriptID = models.CharField(max_length=255)
    transcriptIndex = models.CharField(max_length=255)
    areaType = models.CharField(max_length=255)
    start = models.IntegerField()
    end = models.IntegerField()
    length = models.IntegerField()
    transcriptRange = models.CharField(max_length=255)
    transcriptLength = models.IntegerField()
    nucleotideSequence = models.TextField()
    proteinSequence = models.TextField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'transcript'
        managed = False

    def __str__(self):
        return f"{self.mosaicID}"  # 用于返回模型的字符串表示，例如在admin界面显示
    
class mosaicTPM(models.Model):
    mosaicID = models.CharField(max_length=255)
    Ca1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'mosaic_tpm'
        managed = False

    def __str__(self):
        return f"{self.mosaicID}" # 用于返回模型的字符串表示，例如在admin界面显示
    
class xenologousTPM(models.Model):
    mosaicID = models.CharField(max_length=255)
    xenologousID = models.CharField(max_length=255)
    Ca1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'xenologous_tpm'
        managed = False

    def __str__(self):
        return f"{self.xenologousID}" # 用于返回模型的字符串表示，例如在admin界面显示
    
class geneTPM(models.Model):
    mosaicID = models.CharField(max_length=255)
    xenologousID = models.CharField(max_length=255)
    geneID = models.CharField(max_length=255)
    Ca1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gene_tpm'
        managed = False

    def __str__(self):
        return f"{self.geneID}" # 用于返回模型的字符串表示，例如在admin界面显示

class transcriptTPM(models.Model):
    mosaicID = models.CharField(max_length=255)
    xenologousID = models.CharField(max_length=255)
    geneID = models.CharField(max_length=255)
    transcriptID = models.CharField(max_length=255)
    Ca1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ca3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Ro2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    NR1_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    AM_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Sp_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Br_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    St_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Pi_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Gl_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    LS2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    In2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    No2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Bu3_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_1 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_2 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    Le2_3 = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'transcript_tpm'
        managed = False

    def __str__(self):
        return f"{self.transcriptID}" # 用于返回模型的字符串表示，例如在admin界面显示

class GT42GenomeID(models.Model):
    genomeID = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_genome_id'
        managed = False

    def __str__(self):
        return f"{self.genomeID}"  # 用于返回模型的字符串表示，例如在admin界面显示
    
class GT42NextID(models.Model):
    id = models.AutoField(primary_key=True)
    nextID = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    class Meta:
        db_table = 'gt42_next_id'
        managed = False

    def __str__(self):
        return f"{self.nextID}"  # 用于返回模型的字符串表示，例如在admin界面显示
    
class GT42MosaicNetworkNodes(models.Model):
    name = models.CharField(max_length=255)
    symbolSize = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    color = models.CharField(max_length=255)
    totalDegree = models.IntegerField()
    inDegree = models.IntegerField()
    outDegree = models.IntegerField()
    adjacency = models.TextField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_mosaic_network_nodes'
        managed = False

    def __str__(self):
        return f"{self.name}"
    
class GT42MosaicNetworkEdges(models.Model):
    source = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    width = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    color = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_mosaic_network_edges'
        managed = False

    def __str__(self):
        return f"{self.source} -> {self.target}"
    
class GT42XenologousNetworkNodes(models.Model):
    name = models.CharField(max_length=255)
    symbolSize = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    color = models.CharField(max_length=255)
    totalDegree = models.IntegerField()
    inDegree = models.IntegerField()
    outDegree = models.IntegerField()
    adjacency = models.TextField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_xenologous_network_nodes'
        managed = False

    def __str__(self):
        return f"{self.name}"
    
class GT42XenologousNetworkEdges(models.Model):
    source = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    width = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    color = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_xenologous_network_edges'
        managed = False

    def __str__(self):
        return f"{self.source} -> {self.target}"
    
class GT42GeneNetworkNodes(models.Model):
    name = models.CharField(max_length=255)
    symbolSize = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    color = models.CharField(max_length=255)
    totalDegree = models.IntegerField()
    inDegree = models.IntegerField()
    outDegree = models.IntegerField()
    adjacency = models.TextField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_gene_network_nodes'
        managed = False

    def __str__(self):
        return f"{self.name}"
    
class GT42GeneNetworkEdges(models.Model):
    source = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    width = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    color = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_gene_network_edges'
        managed = False

    def __str__(self):
        return f"{self.source} -> {self.target}"

class GT42HomologousID(models.Model):
    genomeID = models.CharField(max_length=255)
    homologousIDSet = models.TextField()
    id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'gt42_homologous_id'
        managed = False

    def __str__(self):
        return f"{self.genomeID}"