from urllib import parse
from typing import List, Union


class Url:

    def __init__(self, url: str = ""):
        parse_result = parse.urlparse(str(url))
        self.scheme: str = parse_result.scheme
        self.netloc: str = parse_result.netloc
        self.path: str = parse_result.path
        self.params: str = parse_result.params
        self.query: str = parse_result.query
        self.fragment: str = parse_result.fragment

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    @property
    def path_list(self) -> List[str]:
        return self.path.lstrip("/").split("/")

    @property
    def query_params(self) -> dict:
        return dict(parse.parse_qsl(self.query))

    @property
    def unquoted_url(self) -> "Url":
        return Url(parse.unquote(str(self)))

    @property
    def filename(self) -> str:
        return self.path_list[-1]

    def __str__(self) -> str:
        return parse.urlunparse(
            (
                self.scheme,
                self.netloc,
                self.path,
                self.params,
                self.query,
                self.fragment,
            )
        )

    def __repr__(self) -> str:
        return (
            f"WUrl(scheme={self.scheme}, "
            f"netloc={self.netloc}, "
            f"path={self.path}, "
            f"params={self.params}, "
            f"query={self.query}, "
            f"fragment={self.fragment})"
        )

    def __setitem__(self, key: Union[str, int], value: str) -> None:
        if isinstance(key, int):
            path_list = self.path_list
            path_list[key] = value
            self.path = "/".join(path_list)
        else:
            query_dict = self.query_params
            query_dict[key] = value
            self.query = parse.urlencode(query_dict)

    def __delitem__(self, key: Union[str, int]) -> None:
        if isinstance(key, int):
            path_list = self.path_list
            del path_list[key]
            self.path = "/".join(path_list)
        else:
            query_dict = self.query_params
            del query_dict[key]
            self.query = parse.urlencode(query_dict)

    def __getitem__(self, key: Union[str, int]) -> str:
        if isinstance(key, int):
            return self.path_list[key]
        else:
            return self.query_params[key]

    def join(self, *paths: str) -> "Url":
        return Url(parse.urljoin(str(self), "/".join(paths)))

    def copy(self) -> "Url":
        return Url(str(self))
