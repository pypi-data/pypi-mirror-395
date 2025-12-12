from slugify import slugify
from orion.databases.db_empatia.utils import generate_slug


res= generate_slug("lugar", 'Batallon de Ingenieros de Desminado Humanitario N° 7 " Cr. Gabino Gutierrez" (BIDEH7)')
print(res)
res = slugify('Batallon de Ingenieros de Desminado Humanitario N° 7 " Cr. Gabino Gutierrez" (BIDEH7)')
print(res)
