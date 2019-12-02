from unittest import TestCase

from pytrendsasync.request import TrendReq
import asyncio
import pytest
from pytrendsasync.dailydata import get_daily_data
from datetime import date

TIMEOUT = 30

class TestTrendReq:

    @pytest.mark.asyncio
    async def test_get_data(self):
        """Should use same values as in the documentation"""
        pytrend = TrendReq(timeout=TIMEOUT)
        assert pytrend.hl == 'en-US'
        assert pytrend.tz == 360
        assert pytrend.geo == ''

    @pytest.mark.asyncio
    async def test_get_cookie_on_request(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        await pytrend.interest_over_time()
        assert pytrend.cookies['NID']
    
    @pytest.mark.asyncio
    async def test_build_payload(self):
        """Should return the widgets to get data"""
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        assert pytrend.token_payload is not None

    @pytest.mark.asyncio
    async def test_tokens(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        assert pytrend.related_queries_widget_list != None

    @pytest.mark.asyncio
    async def test_interest_over_time(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        resp = await pytrend.interest_over_time()
        assert resp is not None

    @pytest.mark.asyncio
    async def test_interest_by_region(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        interest = await pytrend.interest_by_region()
        assert interest is not None

    @pytest.mark.asyncio
    async def test_related_topics(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        related_topics = await pytrend.related_topics()
        assert related_topics is not None

    @pytest.mark.asyncio
    async def test_related_queries(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        related_queries = await pytrend.related_queries()
        assert related_queries is not None

    @pytest.mark.asyncio
    async def test_trending_searches(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        trending_searches = await pytrend.trending_searches(pn='united_states')
        assert trending_searches is not None

    @pytest.mark.asyncio
    async def test_top_charts(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        top_charts = await pytrend.top_charts(date=2016)
        assert top_charts is not None

    @pytest.mark.asyncio
    async def test_suggestions(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        suggestions = await pytrend.suggestions(keyword='pizza')
        assert suggestions is not None

class TestDailyData:

    @pytest.mark.asyncio
    async def test_daily_data(self):
        d1 = date(2018, 6, 1)
        d2 = date(2018, 12, 31)
        day_count = (d2 - d1).days + 1

        data = await get_daily_data(
            'cat', d1.year, d1.month, 
            d2.year, d2.month, wait_time=3)
        assert data is not None
        assert len(data) == day_count
        