import asyncio
import datetime
from unittest import mock
import logging

import pytest

from nrk_api.cli import browse, expires_at, parse, search


async def resp(r):
    """Helper for side effect"""
    return r


def test_search(runner, nrk):
    nrk.cli = False
    nrk.subtitle = True
    with mock.patch('nrk_api.helpers.prompt_async', side_effect=[resp('0'), resp('1')]):
        with mock.patch('nrk_api.cli.prompt_async', side_effect=[resp('y')]):

            async def gogo():
                await search(nrk, 'skam')
                assert len(nrk.downloads())

            runner(asyncio.wait([gogo()]))


def test_expires_at(runner, fresh_nrk):
    today = datetime.date.today()
    next_mounth = today + datetime.timedelta(weeks=2)
    time_periode = '%s-%s' % (today.strftime("%d.%m.%Y"), next_mounth.strftime("%d.%m.%Y"))
    fresh_nrk.cli = False
    fresh_nrk.subtitle = True
    fresh_nrk.downloads().clear()

    with mock.patch('nrk_api.helpers.prompt_async', side_effect=[resp('0')]):
        with mock.patch('nrk_api.cli.prompt_async', side_effect=[resp('y')]):
            async def gogo():
                await expires_at(fresh_nrk, time_periode)
                assert len(fresh_nrk.downloads()) == 1

            runner(gogo())


def test_browse(runner, fresh_nrk):
    fresh_nrk.downloads().clear()
    fresh_nrk.cli = False
    fresh_nrk.subtitle = True
    with mock.patch('nrk_api.helpers.prompt_async', side_effect=[resp('0'), resp('0'), resp('0')]):
        with mock.patch('nrk_api.cli.prompt_async', side_effect=[resp('all'), resp('y')]):
            async def gogo():
                await browse(fresh_nrk)
                assert len(fresh_nrk.downloads()) == 1

            runner(gogo())

def test_parse(runner, fresh_nrk):
    fresh_nrk.cli = False
    fresh_nrk.subtitle = True
    fresh_nrk.downloads().clear()
    async def gogo():
        await parse(fresh_nrk, 'https://tv.nrk.no/serie/skam/MYNT15000117/sesong-4/episode-1 http://tv.nrksuper.no/serie/kash-og-zook https://tv.nrk.no/program/KOID22009417/plasthvalen'.split())
        assert len(fresh_nrk.downloads()) == 3

    runner(gogo())
