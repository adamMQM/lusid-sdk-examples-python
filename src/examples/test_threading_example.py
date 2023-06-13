import lusid
import asyncio
import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def application_metadata_api(api_client_factory):
    return api_client_factory.build(lusid.ApplicationMetadataApi)
    # close connection pool


class TestAsyncExamples:
    @pytest.mark.asyncio
    async def test_get_lusid_version_async(self, application_metadata_api):
        """Send request to get lusid version asyncronously

        Args:
            application_metadata_api (lusid.api.ApplicationMetadataApi): api object used to send request to ApplicationMetadata endpoints

        Returns:
            lusid.model.version_summary_dto.VersionSummaryDto: The summary of the running lusid version
        """
        # no longer need to call with async_req = True
        # calling with async_req = True will execute request using a ThreadPool
        # which is generally less efficient than running single-threaded with
        # asyncio and aiohttp due to the overhead of context-switching and threads not
        # running on multiple cores due to the Python GIL.
        # Kicks off a coroutine, which sends a request
        # the result of which is awaited on by asyncio.
        async_result = await application_metadata_api.get_lusid_versions()
        assert async_result is not None

    @pytest.mark.asyncio
    async def test_get_lusid_version_multithreaded(self, application_metadata_api):
        """Send request to get lusid version asyncronously using multithreading

        Args:
            application_metadata_api (lusid.api.ApplicationMetadataApi): api object used to send request to ApplicationMetadata endpoints

        Returns:
            multiprocessing.pool.AsyncResult: An object with methods to monitor execution of a function in a threadpool,
            and retreive the result of the function execution
        """
        # calling without await calls synchronous version automatically
        num_requests = 10
        multiple_requests = (
            application_metadata_api.get_lusid_versions(async_req=True)
            for i in range(num_requests)
        )
        result = await asyncio.gather(
            *(result_thread.get() for result_thread in multiple_requests)
        )
        assert len(result) == num_requests
