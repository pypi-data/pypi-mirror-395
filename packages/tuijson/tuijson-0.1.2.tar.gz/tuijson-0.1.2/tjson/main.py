import sys
from tjson import T_JSON, load_json_input


def check_at_least_one_arg():
    if len(sys.argv) < 2:
        sys.exit("Usage: treejson <json_string_or_filepath> OPTIONAL:<json_string_or_filepath2>")


def load_json_from_args():
    json1 = load_json_input(sys.argv[1])
    json2 = (None, "")
    if len(sys.argv[1:]) > 1:
        json2 = load_json_input(sys.argv[2])
    return json1, json2
    

def main():
    check_at_least_one_arg()    
    json1, json2 = load_json_from_args()
    app = T_JSON(*json1, *json2)
    app.run()


if __name__ == "__main__":
    main()
