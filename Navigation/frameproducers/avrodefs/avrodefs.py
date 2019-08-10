from confluent_kafka import avro

value_schema_str = """
{
   "namespace": "frames.avro",
   "name": "FramesV8",
   "type": "record",
   "fields" : [
     {"name" : "frame", "type" : "bytes"},
     {"name" : "shape", "type" : {"type" : "array", "items" : "int"}}
   ]
}
"""

key_schema_str = """
{
   "namespace": "keys.avro",
   "name": "KeysV8",
   "type": "record",
   "fields" : [
     {"name" : "key", "type" : "string"}
   ]
}
"""


value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)
