import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

df = spark.read.option("header", "true").option("delimiter", ";").csv(
    "s3://analisis-productos-alimenticios-data/raw/")

lista_categorias_descartadas = [
    "Velas", "Pañal talla de 4 a XL", "Braguita y otros", "Toallitas",
    "Pañal talla de 0 a 3", "Accesorios", "Biberón", "Chupete",
    "Aceite y crema", "Champú y jabón", "Colonia",
    "Cápsulas compatibles Tassimo", "Hierbas", "Colorante y pimentón", "Hielo"
]
ean_productos_eliminar = [8480000828422, 8480000676603]

df_columnas_importantes = df.filter(
    ~F.col("categoria").isin(lista_categorias_descartadas))
df_columnas_importantes = df_columnas_importantes.filter(
    ~F.col("ean").isin(ean_productos_eliminar))

df_filtrado = df_columnas_importantes

columnas_nutricionales = ["calorias_100g", "proteinas_100g",
                          "azucar_100g", "fibra_100g", "grasa_saturada_100g", "sal_100g"]
for col_name in columnas_nutricionales:
    df_filtrado = df_filtrado.withColumn(
        col_name, F.col(col_name).cast("double"))

df_filtrado = df_filtrado.withColumn(
    "procesado",
    F.when(F.col("procesado") == "{}", None).otherwise(
        F.col("procesado")).cast("int")
)

dynamic_frame_silver = DynamicFrame.fromDF(
    df_filtrado, glueContext, "dynamic_frame_silver")

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_silver,
    connection_type="s3",
    connection_options={
        "path": "s3://analisis-productos-alimenticios-data/silver/",
        "purge": "True"
    },
    format="parquet"
)

job.commit()
