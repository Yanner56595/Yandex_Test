from geo_func import get_coords, show_map, find_store


def main():
    toponym = input()
    try:
        lat, lon = get_coords(toponym)
        lat_drug, lon_drug, information = find_store(f'{lat},{lon}')
        points = f'{lat},{lon},pmwtm1~{lat_drug},{lon_drug},pmwtm2'
        type_map = 'map'
        for elem in information:
            print(elem, information[elem])
        show_map(type_map, points)
    except Exception as e:
        print('Error', e)


if __name__ == '__main__':
    main()