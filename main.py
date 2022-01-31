from geo_func import get_coords, show_map, find_store


def main():
    toponym = input()
    try:
        lat, lon = get_coords(toponym)
        points_drug = find_store(f'{lat},{lon}')
        type_map = 'map'
        show_map(type_map, points_drug)
    except Exception as e:
        print('Error', e)


if __name__ == '__main__':
    main()