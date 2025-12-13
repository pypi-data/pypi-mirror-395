import requests
import json
from com.phida.main.sparksession import spark


def updateJobPermissions(domain, jsonPermission, jobId, token):
    """
        desc:
            A method for updating permission for a Databricks Job

        args:
            domain: String - a string to indentify the databricks workspace
            jsonPermission: String - string in JSON with the permissions
            jobId: String -  the Id for the job cluster to be updated
            token: String - personal access token to execute the request

        return:
            reponse: String - the reponse from Job API call

        example:
            json = {
                            "access_control_list": [
                              {
                                "group_name": "<group name>",
                                "permission_level": "CAN_MANAGE_RUN"
                              }]}
            updateJobPermissions("XXXXXXXXX.X.azuredatabricks.net", json,  "<job id>", "my_personal_access_token")
  """
    url =  'https://'+ domain + '/api/2.0/permissions/jobs/' + jobId
    response = requests.put(
        url,
        headers={'Authorization': 'Bearer %s' % token},
        json=jsonPermission
    )
    return response.text