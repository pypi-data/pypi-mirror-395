import xml.etree.ElementTree as ET
from wp21_train.utils.version import __version__

class hls_parser:

    def __init__(self, report_name, block_name = 'top'):        
        self._rpt_name  = report_name
        self._fw_block  = block_name
        self._data      = {}
        self._meta_data = {}
        self._parse('AreaEstimates'       )
        self._parse('UserAssignments'     )
        self._parse('PerformanceEstimates')

    def _parse(self, _criterion = 'AreaEstimates'):
        tree = ET.parse(self._rpt_name)
        root = tree.getroot()

        elem = root.find(_criterion)

        if _criterion == 'AreaEstimates':
            for i_elem in elem:
                if i_elem.tag == 'Resources':
                    for i_resource in i_elem:
                        self._data[i_resource.tag] = float(i_resource.text.strip())
                elif i_elem.tag == 'AvailableResources':
                    for i_resource in i_elem:
                        self._meta_data[i_resource.tag] = float(i_resource.text.strip())
        elif _criterion == 'UserAssignments':
            for i_elem in elem:
                self._meta_data[i_elem.tag] = i_elem.text.strip()
        elif _criterion == 'PerformanceEstimates':
            for i_elem in elem:
                if i_elem.tag == 'SummaryOfTimingAnalysis':
                    self._data['EstimatedClockPeriod'] = float(i_elem.find('EstimatedClockPeriod').text.strip())
                elif i_elem.tag == 'SummaryOfOverallLatency':
                    self._data['BestCaseLatency']    = float(i_elem.find('Best-caseLatency')   .text.strip())
                    self._data['AverageCaseLatency'] = float(i_elem.find('Average-caseLatency').text.strip())
                    self._data['WorstCaseLatency']   = float(i_elem.find('Worst-caseLatency')  .text.strip())
                    self._data['PipelineDepth']      = float(i_elem.find('PipelineDepth')      .text.strip())

    def get_version(self):
        return f"hls_parser version: {__version__}"
