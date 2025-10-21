from collections import deque

class SocialNetwork:
    def __init__(self, graph):
        self.graph = graph

    def find_friends_at_distance(self, start, distance):
        visited = set()
        queue = deque([(start, 0)])
        result = []

        while queue:
            current, dist = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            if dist == distance:
                result.append(current)
            elif dist < distance:
                for neighbor in self.graph.get(current, []):
                    if neighbor not in visited:
                        queue.append((neighbor, dist + 1))

        return result

    def are_connected(self, person_a, person_b, max_depth=6):
        visited = set()
        queue = deque([(person_a, 0)])

        while queue:
            current, depth = queue.popleft()
            if current == person_b:
                return True
            if depth >= max_depth:
                continue
            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
        return False

class WebCrawler:
    def __init__(self, web):
        self.web = web

    def crawl(self, start_url, max_depth):
        visited = set()

        def dfs(url, depth):
            if depth > max_depth or url in visited:
                return
            visited.add(url)
            for link in self.web.get(url, []):
                dfs(link, depth + 1)

        dfs(start_url, 0)
        return visited

    def find_route(self, page_a, page_b):
        from collections import deque

        queue = deque([(page_a, [page_a])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            if current == page_b:
                return path
            visited.add(current)
            for neighbor in self.web.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None


social_graph = {
    'Alice': ['Bob', 'Claire'],
    'Bob': ['Alice', 'Dan', 'Eve'],
    'Claire': ['Alice', 'Frank'],
    'Dan': ['Bob'],
    'Eve': ['Bob'],
    'Frank': ['Claire']
}

sn = SocialNetwork(social_graph)

print(sn.find_friends_at_distance('Alice', 2))
print(sn.are_connected('Alice', 'Frank'))      
print(sn.are_connected('Alice', 'Zoe'))

web_graph = {
    'home': ['about', 'products', 'contact'],
    'about': ['team', 'careers'],
    'products': ['product1', 'product2'],
    'team': [],
    'careers': [],
    'contact': ['form'],
    'form': [],
    'product1': [],
    'product2': ['form']
}

crawler = WebCrawler(web_graph)

print(crawler.crawl('home', 2))
print(crawler.find_route('home', 'form'))
