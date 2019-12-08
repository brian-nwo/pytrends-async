from unittest import TestCase

from pytrendsasync.request import TrendReq
import asyncio
import pytest
from pytrendsasync.dailydata import get_daily_data
from pytrendsasync.exceptions import ResponseError
import pytrendsasync
from datetime import date
from httpx.models import Response
import httpx
from httpx.exceptions import ProxyError
import proxy
from asynctest.mock import patch, CoroutineMock, MagicMock, Mock, call, ANY
from asyncio.futures import Future

TIMEOUT = 30

@pytest.mark.asyncio
class TestTrendReq:
    async def test_get_data(self):
        """Should use same values as in the documentation"""
        pytrend = TrendReq(timeout=TIMEOUT)
        assert pytrend.hl == 'en-US'
        assert pytrend.tz == 360
        assert pytrend.geo == ''

    async def test_get_cookie_on_request(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        await pytrend.interest_over_time()
        assert pytrend.cookies['NID']
    
    async def test_build_payload(self):
        """Should return the widgets to get data"""
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        resp = await pytrend.interest_over_time()
        assert pytrend.token_payload is not None

    async def test_tokens(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        assert pytrend.related_queries_widget_list != None

    async def test_interest_over_time(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        resp = await pytrend.interest_over_time()
        assert resp is not None

    async def test_interest_by_region(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        interest = await pytrend.interest_by_region()
        assert interest is not None

    async def test_related_topics(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        related_topics = await pytrend.related_topics()
        assert related_topics is not None

    async def test_related_queries(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        related_queries = await pytrend.related_queries()
        assert related_queries is not None

    async def test_trending_searches(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        trending_searches = await pytrend.trending_searches(pn='united_states')
        assert trending_searches is not None

    async def test_top_charts(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        top_charts = await pytrend.top_charts(date=2016)
        assert top_charts is not None

    async def test_suggestions(self):
        pytrend = TrendReq(timeout=TIMEOUT)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        suggestions = await pytrend.suggestions(keyword='pizza')
        assert suggestions is not None

    @patch('pytrendsasync.request.Client')
    async def test_all_retries_fail(self, client_mock):
        client_mock.return_value.__aenter__.return_value = client_mock
        client_mock.get = CoroutineMock(return_value=Response(status_code=429))

        pytrend = TrendReq(timeout=TIMEOUT, retries=3, backoff_factor=0.1)
        with pytest.raises(ResponseError):
            await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        
        calls = [call('https://trends.google.com/?geo=US', timeout=ANY) for _ in range(pytrend.retries)]
        client_mock.get.assert_has_calls(calls)
    
    @patch('pytrendsasync.request.Client')
    async def test_retry_initially_fail_then_succeed(self, client_mock, trending_searches_200_response):
        client_mock.return_value.__aenter__.return_value = client_mock
        pytrend = TrendReq(retries=3, backoff_factor=0.1)
        pytrend.cookies = {'NID': '12eqf98hnf8032r54'}
        retry_count = 0

        async def _get_request_side_effect(url, *args, **kwargs):
            nonlocal retry_count
            retry_count += 1
            #Make fail in a few different ways. On last attempt, return response
            if retry_count == pytrend.retries - 1:
                raise ConnectionRefusedError()
            elif retry_count != pytrend.retries:
                return Response(status_code=429)
            else:
                return trending_searches_200_response

        client_mock.get = CoroutineMock(side_effect=_get_request_side_effect)
        trending_searches = await pytrend.trending_searches(pn='united_states')
        assert trending_searches is not None
    
    @patch('pytrendsasync.request.Client')
    async def test_receive_error_no_retries_configured(self, client_mock):
        client_mock.return_value.__aenter__.return_value = client_mock
        client_mock.get = CoroutineMock(return_value=Response(status_code=429))

        pytrends = TrendReq(retries=0, backoff_factor=0)
        pytrends.cookies = {'NID': '12eqf98hnf8032r54'}

        with pytest.raises(ResponseError):
            await pytrends.top_charts(date=2018)
        assert client_mock.get.call_count == 1


@pytest.mark.asyncio
class TestTrendReqWithProxies:
    async def test_send_req_through_proxy(self, create_proxy):
        create_proxy('127.0.0.1', 8899)
        pytrend = TrendReq(timeout=TIMEOUT, proxies=['http://127.0.0.1:8899'])
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        resp = await pytrend.interest_over_time()
        assert resp is not None

    async def test_proxy_cycling(self, create_proxy):
        create_proxy('127.0.0.1', 8899)
        create_proxy('127.0.0.1', 8900)
        create_proxy('127.0.0.1', 8901)
        proxies = ['http://127.0.0.1:8899', 'http://127.0.0.1:8900', 'http://127.0.0.1:8901']

        pytrend = TrendReq(timeout=TIMEOUT, proxies=proxies)
        last_proxy = pytrend._get_proxy()

        await pytrend.suggestions(keyword='pizza')
        curr_proxy = pytrend._get_proxy()
        assert curr_proxy != last_proxy
        last_proxy = curr_proxy

        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        curr_proxy = pytrend._get_proxy()
        assert curr_proxy != last_proxy
        last_proxy = curr_proxy

        await pytrend.interest_over_time()
        curr_proxy = pytrend._get_proxy()
        assert curr_proxy != last_proxy
        
    @patch('pytrendsasync.request.Client')
    async def test_proxy_cycle_on_429_no_blacklist(self, client_mock):
        client_mock.return_value.__aenter__.return_value = client_mock
        proxies = ['http://127.0.0.1:8899', 'http://127.0.0.1:8900']
        retry_count = 0

        async def _get_request_side_effect(url, *args, **kwargs):
            nonlocal retry_count
            retry_count += 1
            if retry_count <= len(proxies):
                raise ProxyError(response=Response(status_code=429))
            else:
                return Response(status_code=429)

        client_mock.get = CoroutineMock(side_effect=_get_request_side_effect)
        pytrend = TrendReq(timeout=TIMEOUT, proxies=proxies)
        with pytest.raises(ResponseError):
            await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        
        #Ensure we sent req to proxies, and then w/o proxy once proxies exausted
        for proxy in proxies:
            client_mock.assert_any_call(proxies={'all': proxy})
        client_mock.assert_called_with(proxies=None)

        #Proxies that returned 429 should still be available in proxy list
        assert pytrend.proxies.sort() == proxies.sort()
        assert len(pytrend.blacklisted_proxies) == 0

    async def test_blacklist_proxy_on_failure(self, create_proxy):
        proxies = ['http://127.0.0.1:2391']
        pytrend = TrendReq(timeout=TIMEOUT, proxies=proxies)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        assert pytrend._get_proxy() is None
        assert len(pytrend.proxies) == 0
        assert len(pytrend.blacklisted_proxies) == len(proxies)

    async def test_fallback_to_local_requests_on_last_proxy_failure(self):
        proxies = ['http://127.0.0.1:2391', 'http://127.0.0.1:2390']
        pytrend = TrendReq(timeout=TIMEOUT, proxies=proxies)
        await pytrend.build_payload(kw_list=['pizza', 'bagel'])
        resp = await pytrend.interest_over_time()
        assert len(pytrend.proxies) == 0
        assert len(pytrend.blacklisted_proxies) == len(proxies)
        assert resp is not None 

        
@pytest.mark.asyncio
class TestDailyData:
    async def test_daily_data(self):
        d1 = date(2018, 6, 1)
        d2 = date(2018, 12, 31)
        day_count = (d2 - d1).days + 1

        data = await get_daily_data(
            'cat', d1.year, d1.month, 
            d2.year, d2.month, wait_time=3)
        assert data is not None
        assert len(data) == day_count
        