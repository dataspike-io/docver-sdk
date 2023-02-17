from uuid import UUID

from conftest import to_json
from dataspike import Applicant, ApplicantInfo, Api, PagedResponse


async def test_applicant_get(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    applicant = Applicant(applicant_id=applicant_id, display_info=ApplicantInfo(full_name="John Doe"))
    body = to_json(applicant)

    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}", body=body)

    got = await api.applicant.get(applicant_id)
    aioresponses.assert_called_once()
    assert got == applicant


async def test_applicant_find(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    applicant = Applicant(applicant_id=applicant_id, display_info=ApplicantInfo(full_name="John Doe"))
    body = to_json(applicant)

    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}", body=body)

    got = await api.applicant.find(applicant_id)
    aioresponses.assert_called_once()
    assert got == applicant


async def test_applicant_find_return_none(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)
    aioresponses.get(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}", status=404)

    got = await api.applicant.find(applicant_id)
    aioresponses.assert_called_once()
    assert got is None


async def test_applicant_create(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524467342344623421465345)
    aioresponses.post(
        f"https://api.dataspike.io/api/v3/applicants", status=201, body=to_json({"id": str(applicant_id)})
    )

    got = await api.applicant.create()
    aioresponses.assert_called_once()
    assert got == applicant_id


async def test_applicant_list(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524467342344623421465345)
    applicant = Applicant(applicant_id=applicant_id, display_info=ApplicantInfo(full_name="John Doe"))
    data = PagedResponse(data=[applicant], has_next=False)
    aioresponses.get(
        r"https://api.dataspike.io/api/v3/applicants?page=0&limit=10",
        status=200,
        body=to_json(data),
    )

    got = await api.applicant.list()
    aioresponses.assert_called_once()
    assert got == data


async def test_applicant_delete(aioresponses, api: Api):
    applicant_id = UUID(int=21355515246424524622342344623421465345)

    aioresponses.delete(f"https://api.dataspike.io/api/v3/applicants/{applicant_id}")

    await api.applicant.delete(applicant_id)
    aioresponses.assert_called_once()