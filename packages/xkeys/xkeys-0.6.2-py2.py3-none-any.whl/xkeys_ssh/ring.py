# coding:utf-8

from os import listdir
from os import remove
from os import rename
from os.path import exists
from os.path import isfile
from os.path import join
from typing import Iterator
from typing import Optional
from uuid import uuid4

from xkits_lib.cache import CachePool

from xkeys_ssh.pair import SSHKeyAlgo
from xkeys_ssh.pair import SSHKeyPair


class SSHKeyRing():
    def __init__(self, base: Optional[str] = None):
        self.__cache: CachePool[str, SSHKeyPair] = CachePool(lifetime=0)
        self.__base: str = base or "."

    @property
    def base(self) -> str:
        return self.__base

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __iter__(self) -> Iterator[str]:
        for item in listdir(self.base):
            if item.endswith(".tar") and isfile(self.join(name := item[:-4])):
                yield name

    def __contains__(self, name: str) -> bool:
        return name in self.__cache or isfile(self.join(name))

    def __getitem__(self, name: str) -> SSHKeyPair:
        if name not in self.__cache:
            self.__cache.put(name, self.load(name))
        return self.__cache.get(name)

    def __delitem__(self, name: str):
        self.remove(name)

    def join(self, name: str) -> str:
        return join(self.base, f"{name}.tar")

    def seek(self, fingerprint: str) -> Optional[str]:
        return next((key for key in self if self[key].fingerprint == fingerprint), None)  # noqa:E501

    def dump(self, name: str, pair: SSHKeyPair) -> SSHKeyPair:
        if (key := self.seek(pair.fingerprint)) is not None:
            raise FileExistsError(f"SSH key pair '{key}' already exists")

        pair.dump(self.join(name))
        self.__cache.put(name, pair)
        return self.__cache.get(name)

    def load(self, name: str) -> SSHKeyPair:
        return SSHKeyPair.load(self.join(name))

    def remove(self, name: str) -> bool:
        self.__cache.delete(name)
        if exists(path := self.join(name)) and isfile(path):
            remove(path)
        return not exists(path)

    def rename(self, origin: str, target: str) -> bool:
        self.__cache.delete(origin)

        if not isfile(src := self.join(origin)) or exists(dst := self.join(target)):  # noqa:E501
            return False  # pragma: no cover

        rename(src=src, dst=dst)
        return not exists(src) and isfile(dst)

    def update(self, name: str, private: str) -> None:
        if not self.rename(origin=name, target=(backup := f"{name}.old")):
            raise ValueError(f"failed to create '{name}' backup")  # noqa:E501, pragma: no cover

        try:
            self.create(private=private, name=name)
        except Exception:
            self.rename(origin=backup, target=name)
            raise

        if not self.remove(name=backup):
            raise ValueError(f"failed to delete '{name}' backup")  # noqa:E501, pragma: no cover

    def create(self, private: str, name: Optional[str] = None) -> str:
        if not (value := SSHKeyPair(private=private)):
            raise ValueError("invalid private key")  # pragma: no cover

        index: str = name or value.comment or str(uuid4())
        self.dump(name=index, pair=value)
        return index

    def generate(self,  # pylint: disable=R0913,R0917
                 algo: SSHKeyAlgo = "rsa",
                 bits: Optional[int] = None,
                 name: Optional[str] = None,
                 comment: Optional[str] = None,
                 passphrase: Optional[str] = None
                 ) -> str:
        value = SSHKeyPair.generate(algo=algo, bits=bits, comment=comment, passphrase=passphrase)  # noqa:E501
        index = name or comment or str(uuid4())
        self.dump(name=index, pair=value)
        return index


if __name__ == "__main__":
    pass
