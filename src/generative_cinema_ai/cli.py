import argparse
from pathlib import Path
from uuid import UUID

from .models import AnalysisRequest, InputFormat
from .service import AnalysisService


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--tenant-id", type=UUID, default=UUID("00000000-0000-0000-0000-000000000001"))
    parser.add_argument("--project-id", type=UUID, default=UUID("00000000-0000-0000-0000-000000000002"))
    parser.add_argument("--format", choices=[item.value for item in InputFormat], default="auto")
    args = parser.parse_args()
    request = AnalysisRequest(
        tenant_id=args.tenant_id, project_id=args.project_id, screenplay_text=args.path.read_text(encoding="utf-8"), input_format=args.format
    )
    print(AnalysisService().analyze(request).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
