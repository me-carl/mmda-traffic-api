from xml.etree import ElementTree


class Feed:
    traffic = {}

    def __init__(self, content):
        root = ElementTree.fromstring(content)
        channel = root.find('channel')
        items = channel.findall('item')

        for item in items:
            title = item.find('title').text
            description = item.find('description').text
            pub_date = item.find('pubDate').text
            highway, segment, direction = self._parse_title(title)

            _highway = self.traffic.get(highway)
            if not _highway:
                self.traffic[highway] = _highway = {
                    'label': self._parse_name(highway),
                    'segments': {},
                }

            _segment = _highway.get('segments').get(segment)
            if not _segment:
                _highway.get('segments')[segment] = _segment = {
                    'label': self._parse_name(segment),
                    'traffic': {},
                }

            traffic = _segment.get('traffic')
            traffic[direction] = {
                'label': self._parse_direction(direction),
                'status': self._parse_status(description),
                'updated_at': pub_date,
            }

    def _parse_title(self, title):
        parts = title.split('-')
        last_index = len(parts) - 1

        highway = parts[0]
        segment = '-'.join(parts[1:last_index])
        direction = parts[last_index]

        return highway, segment, direction

    def _parse_name(self, name):
        name = name.replace('_', ' ')
        name = name.replace('AVE.', 'Avenue')
        name = name.replace('BLVD.', 'Boulevard')

        if name not in ['EDSA', 'U.N.']:
            name = name.title()

        return name

    def _parse_direction(self, direction):
        directions = {
            'NB': 'Northbound',
            'SB': 'Southbound',
        }
        return directions.get(direction)

    def _parse_status(self, status):
        statuses = {
            'L': 'Light',
            'ML': 'Light to Moderate',
            'M': 'Moderate',
            'MH': 'Moderate to Heavy',
            'H': 'Heavy',
        }
        return statuses.get(status)

    def items(self):
        return [self.traffic]
