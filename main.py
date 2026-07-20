"""HTTP entry point for the monthly healthcare data refresh."""

import functions_framework

from run_all_pipelines import run_all


@functions_framework.http
def monthly_pipeline_refresh(request):
    """Run the complete CMS healthcare analytics platform refresh."""
    if request.method != "POST":
        return ("Method not allowed. Use POST.", 405)

    run_all()

    return (
        {
            "status": "success",
            "message": "CMS healthcare analytics platform refresh completed.",
        },
        200,
    )
